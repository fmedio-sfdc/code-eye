Pipeline Architecture

There are many steps required to move from a range of dates we would like to examine to a set of change lists, and files in those change lists, and perforce and gus information about the files and the change lists. At each step of the way we gather more data and more features for our machine learning. The most flexible way to solve this problem is to create a pipeline of processing where output from one step can be fed as input to the next step.

We use JSON dictionaries to store features for each java file that we process. Each step in the pipeline reads a set of json dictionaries and writes the same set of dictionaries, adding some information along the way. In the end the set of dictionaries will be used as input into the machine learning algorithm.

0. Prep shell environment
    1. p4 login
    2. export GUS_SESSION_ID='<session-id>'
1. Retrieve changelists
    1. input: parameters for “p4 changes” cmd, like a range of dates for CL retrieval
    2. output: p4 describe output for each CL
    3. example:
            p4 changes -s submitted //app/main/core/...@2016/11/18,2017/03/30 | awk '{print $2}' | xargs p4 describe -s > changes.out
2. Gather filenames and other features from the p4 describe command
    1. input: file containing changelist info
    2. output: json dict containing filename, gusid, and other p4 info
    3. example:
        python retrieve.py changes.out 2>retrieve.err > retrieve.out
3. Retrieve GUS info
    1. input: streamed
    2. output: gus record type and label= 0 or 1 (based on gus type) added to dicts
    3. create environment variable GUS_SESSION_ID with a valid gus session id
    3. example:
         cat retrieve.out | python gus.py 2>gus.err > gus.out
4. Find java source. When label=1 find previous java version
    1. input: streamed
    2. outupt: substitute pre-bug java filename+version when label=1, skip files where label=0 if file already exists with label=1
    3. example:
        python javasource.py 2>javasource.err > javasource.out
5. Analyze java source
    1. input: streamed
    2. output: add metrics from java parsing
    3. example:
        java -jar /path/to/code-stat/target/java-source-analyzer-1.0-SNAPSHOT.jar 2>parser.err > parser.out

