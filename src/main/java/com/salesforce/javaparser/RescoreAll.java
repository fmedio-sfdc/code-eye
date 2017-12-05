package com.salesforce.javaparser;

import java.io.*;
import java.util.Iterator;
import java.util.function.Consumer;

import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;

import com.google.gson.*;
import com.twitter.common.base.ExceptionalClosure;
import com.twitter.common.io.FileUtils;


public class RescoreAll {
    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            System.err.println("Usage: RescoreAll inputFile rescoredFile");
            System.exit(-1);
        }

        new FileUtils.Temporary(new File(".")).doWithDir((ExceptionalClosure<File, Exception>) dir -> {
            System.err.println("Temp index dir: " + dir.getAbsolutePath());
            Gson gson = new GsonBuilder()
                    .setPrettyPrinting()
                    .disableHtmlEscaping()
                    .create();

            Progress progress = new Progress(100);
            Directory directory = FSDirectory.open(dir.toPath());
            TermStatistics ts = new TermStatistics();
            Iterator<JsonObject> iterator = new FrameParser(new FileInputStream(args[0]));
            System.err.println("Indexing all docs");
            ts.index(iterator, directory, progress);
            System.err.println(" done indexing.");

            IndexReader indexReader = DirectoryReader.open(directory);
            PrintStream ps = new PrintStream(args[1]);
            System.err.println("Rewriting scores");
            iterator = new FrameParser(new FileInputStream(args[0]));
            while (iterator.hasNext()) {
                JsonObject rescored = ts.rescore(indexReader, iterator.next());
                ps.println(gson.toJson(rescored));
                progress.accept(null);
            }
            ps.close();
            System.err.println(" done rewriting scores.");
        });
    }

    static class Progress implements Consumer {
        private final int increment;
        private int count;

        public Progress(int increment) {
            this.increment = increment;
        }

        @Override
        public void accept(Object o) {
            if (count++ % increment == 0) {
                System.err.print(".");
            }
        }
    }
}
