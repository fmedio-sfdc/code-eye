package com.salesforce.mlsandbox

import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.sql.SparkSession

object Train {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession
      .builder()
      .appName("Spark SQL basic example")
      .master("local[2]")
      .getOrCreate()

    // Does not work! Frame is too big!
    val frame = spark.read.json("/Users/fabrice.medio/git/code-eye/data/210-rescored-all-exploded.out")
    frame.show(10)

    val lr = new LogisticRegression()
      .setMaxIter(10)
      .setRegParam(0.3)
      .setElasticNetParam(0.8)

    /// Fit the model
    val lrModel = lr.fit(frame)

    // Print the coefficients and intercept for logistic regression
    println(s"Coefficients: ${lrModel.coefficients} Intercept: ${lrModel.intercept}")
  }
}
