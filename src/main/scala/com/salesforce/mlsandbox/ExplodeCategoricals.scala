package com.salesforce.mlsandbox

import java.io.{FileInputStream, FileOutputStream, PrintStream}
import java.util.function.Consumer
import java.util.zip.GZIPInputStream

import com.google.gson.JsonObject
import com.salesforce.javaparser.FrameParser

object ExplodeCategoricals {
  def main(args: Array[String]): Unit = {
    val parser = new FrameParser(new GZIPInputStream(new FileInputStream("/Users/fabrice.medio/git/code-eye/data/210-rescored-all.out.gz")))
    val rewritten = new PrintStream(new FileOutputStream("/Users/fabrice.medio/git/code-eye/data/210-rescored-all-exploded.out"))

    rewritten.println("[")
    var isFirst = true;

    while (parser.hasNext) {
      val originalObject = parser.next()
      val newJsonObject = new JsonObject()
      val keys = originalObject.keySet()
      keys.forEach(new Consumer[String] {
        override def accept(key: String): Unit = {
          if (key.startsWith("termstatistics.docfrequency") || key.startsWith("termstatistics.termfrequency")) {
            return
          }
          try {
            val numericValue = originalObject.get(key).getAsDouble
            newJsonObject.addProperty(key, numericValue)
          } catch {
            case t: Throwable => {
              val keyName = key + ":" + originalObject.get(key).getAsString
              val value = 1.0d
              newJsonObject.addProperty(keyName, value)
            }
          }
        }
      })

      if (!isFirst) {
        rewritten.println(",")
      }
      isFirst = false;
      rewritten.println(newJsonObject.toString)
    }
    rewritten.println("]")
    rewritten.close()
  }
}
