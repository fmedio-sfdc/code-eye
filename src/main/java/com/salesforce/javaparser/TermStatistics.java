package com.salesforce.javaparser;

import java.io.IOException;
import java.util.Iterator;
import java.util.Map.Entry;
import java.util.Set;
import java.util.function.Consumer;
import java.util.stream.IntStream;

import org.apache.lucene.document.*;
import org.apache.lucene.index.*;
import org.apache.lucene.search.similarities.ClassicSimilarity;
import org.apache.lucene.store.Directory;

import com.google.gson.*;

public class TermStatistics {
    private ClassicSimilarity similarity = new ClassicSimilarity();

    public static final String FIELD_NAME = "lexer";

    public void index(Iterator<JsonObject> iterator, Directory directory, Consumer<Document> docListener) throws IOException {
        IndexWriter indexWriter = new IndexWriter(directory, new IndexWriterConfig());

        while (iterator.hasNext()) {
            Document doc = new Document();
            JsonObject o = iterator.next();
            o.entrySet().stream()
                    .filter(x -> x.getKey().startsWith("lexer."))
                    .flatMap(x -> {
                        int termFreq = (int) x.getValue().getAsDouble();
                        return IntStream.range(0, termFreq)
                                .mapToObj(i -> new Field(FIELD_NAME, x.getKey(), StringField.TYPE_NOT_STORED));
                    })
                    .forEach(f -> doc.add(f));
            indexWriter.addDocument(doc);
            docListener.accept(doc);
        }

        indexWriter.commit();
        indexWriter.close();
    }


    public JsonObject rescore(IndexReader indexReader, JsonObject jsonObject) throws IOException {
        float numTerms = jsonObject.entrySet().stream()
                .filter(x -> x.getKey().startsWith("lexer."))
                .mapToInt(x -> (int) x.getValue().getAsDouble())
                .sum();

        JsonObject rescored = new JsonObject();

        Set<Entry<String, JsonElement>> entries = jsonObject.entrySet();
        rescored.add("termstatistics.documentlength", new JsonPrimitive((int) numTerms));
        for (Entry<String, JsonElement> entry : entries) {
            if (entry.getKey().startsWith("lexer.")) {
                float termFrequency = entry.getValue().getAsFloat();
                long docFrequency = indexReader.docFreq(new Term(FIELD_NAME, entry.getKey()));
                float tf = similarity.tf((termFrequency / numTerms));
                float idf = similarity.idf(docFrequency, indexReader.numDocs());
                float score = tf * idf * idf;
                rescored.addProperty("termstatistics.termfrequency." + entry.getKey(), (int) termFrequency);
                rescored.addProperty("termstatistics.docfrequency." + entry.getKey(), (int) docFrequency);
                rescored.addProperty("termstatistics.tfidf." + entry.getKey(), score);
            } else {
                rescored.add(entry.getKey(), entry.getValue());
            }
        }
        return rescored;
    }
}
