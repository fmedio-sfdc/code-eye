Pipeline Architecture

There are many steps required to move from a range of dates we would like to examine to a set of change lists, and files in those change lists, and perforce and gus information about the files and the change lists. At each step of the way we gather more data and more features for our machine learning. The most flexible way to solve this problem is to create a pipeline of processing where output from one step can be fed as input to the next step.

We use JSON dictionaries to store features for each java file that we process. Each step in the pipeline reads a set of json dictionaries and writes the same set of dictionaries, adding some information along the way. In the end the set of dictionaries will be used as input into the machine learning algorithm.

0. Prep shell environment
    1. p4 login
    2. export GUS_SESSION_ID='<session-id>'

1. Retrieve changelists
    input: parameters for “p4 changes” cmd, like a range of dates for CL retrieval
    output: p4 describe output for each CL
    examples:
        p4 changes -s submitted //app/main/core/...@2016/11/18,2017/03/30 | awk '{print $2}' | xargs p4 describe -s > changes-208-main.out
        p4 changes -s submitted "//app/208/patch/...@>2017/03/31" | awk '{print $2}' | xargs p4 describe -s > changes-208-patch.out

        p4 changes -s submitted //app/main/core/...@2017/03/31,2017/07/27 | awk '{print $2}' | xargs p4 describe -s > changes-210-main.out
        p4 changes -s submitted "//app/210/patch/...@>2017/07/28" | awk '{print $2}' | xargs p4 describe -s > changes-210-patch.out

        p4 changes -s submitted //app/main/core/...@2017/07/28,2017/11/16 | awk '{print $2}' | xargs p4 describe -s > changes-212-main.out
        p4 changes -s submitted "//app/212/patch/...@>2017/11/17" | awk '{print $2}' | xargs p4 describe -s > changes-212-patch.out

2. Gather filenames and other features from the p4 describe command
    input: file containing changelist info
    output: json dict containing filename, gusid, and other p4 info
    examples:
        python retrieve.py changes-208-main.out 2> >(tee retrieve.err) > retrieve-208-main.out
        python retrieve.py changes-208-patch.out 2> >(tee retrieve-patch.err) > retrieve-208-patch.out

        python retrieve.py changes-210-main.out 2> >(tee retrieve.err) > retrieve-210-main.out
        python retrieve.py changes-210-patch.out 2> >(tee retrieve-patch.err) > retrieve-210-patch.out

        python retrieve.py changes-212-main.out 2> >(tee retrieve.err) > retrieve-212-main.out
        python retrieve.py changes-212-patch.out 2> >(tee retrieve-patch.err) > retrieve-212-patch.out

3. Retrieve GUS info
    input: streamed
    output: gus record type
    setup: create environment variable GUS_SESSION_ID with a valid gus session id (see Step 0.)
    examples:
         cat retrieve-208-main.out | python queryGus.py 2> >(tee queryGus.err) > gus-fixes-208-main.out
         cat retrieve-208-patch.out | python queryGus.py 2> >(tee queryGus.err) > gus-fixes-208-patch.out

         cat retrieve-210-main.out | python queryGus.py 2> >(tee queryGus.err) > gus-fixes-210-main.out
         cat retrieve-210-patch.out | python queryGus.py 2> >(tee queryGus.err) > gus-fixes-210-patch.out

         cat retrieve-212-main.out | python queryGus.py 2> >(tee queryGus.err) > gus-fixes-212-main.out
         cat retrieve-212-patch.out | python queryGus.py 2> >(tee queryGus.err) > gus-fixes-212-patch.out

4. Find java source. When label=1 find previous java version
    input: streamed
    output: add feature "label" = [0 or 1], where 1 = Bug or Test Failure and 0 = User Story
            substitute pre-bug java filename+version when label=1, skip files where label=0 if that file version was identified as a pre-bug version
    example:
        cat gus-fixes-208-patch.out gus-fixes-208-main.out gus-fixes-210-patch.out gus-fixes-210-main.out gus-fixes-212-patch.out gus-fixes-212-main.out | python javasource.py 2>  >(tee javasource.err) > javasource-208-210-212-all.out


5. Retrieve GUS info for buggy CLs - this step will replace the existing gus.worktype with the worktype of the gus record associated with the
    input: streamed
    output: gus record type and label= 0 or 1 (based on gus type) added to dicts
    setup: create environment variable GUS_SESSION_ID with a valid gus session id
    example:
        cat javasource-208-210-212-all.out | python queryGus.py 2> >(tee queryGus-bugs.err) > gus-bugs-208-210-212-all.out

6. Add dates
    example
        cat gus-bugs-208-210-212-all.out | python extractDate.py 2> >(tee addDates.err) > extractDates-208-210-212-all.out

Sample data artifact: extractDates-208-210-212-all.out

7. Analyze java source
    input: streamed
    output: add metrics from java parsing
    example:
        cat extractDates-208-210-212-all.out | java -jar ../../../target/java-source-analyzer-1.0-SNAPSHOT.jar 2>parser.err > parser-208-210-212-all.out

Sample data artifact: parser-208-210-212-all.out

8. Rescore java lexer tokens, convert term frequencies to TF-IDF scores
    input: output of 5
    output: same format as input, with tf-idf scores instead of freqs
    example:
        java -cp ../../../target/java-source-analyzer-1.0-SNAPSHOT.jar com.salesforce.javaparser.RescoreAll parser-208-210-212-all.out rescored-208-210-212-all.out


Sample data artifact: rescored-208-210-212-all.out
