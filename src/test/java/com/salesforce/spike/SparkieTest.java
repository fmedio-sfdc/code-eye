package com.salesforce.spike;

import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.junit.Test;

import com.google.common.collect.Lists;

public class SparkieTest {
    @Test
    public void testSpark() {
        JavaSparkContext jsc = new JavaSparkContext("local", "Panda");
        JavaRDD<Integer> rdd = jsc.parallelize(Lists.newArrayList(1, 2, 3, 4))
                .filter(x -> x % 2 == 0);


    }
}