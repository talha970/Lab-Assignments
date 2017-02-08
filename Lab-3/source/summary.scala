

import org.apache.spark.{SparkContext, SparkConf}

/**
 
  */
object SparkWordCount {

  def main(args: Array[String]) {

    System.setProperty("hadoop.home.dir","E:\\winutil");

    val sparkConf = new SparkConf().setAppName("SparkWordCount").setMaster("local[1]")

    val sc=new SparkContext(sparkConf)

    val input=sc.textFile("C:\\Users\\TeeJay\\Documents\\bigdata\\Clarifai\\thetextfile.txt")

    val wc = input.flatMap(line => line.split(" "))
      .map(word => (word, 1))
      .reduceByKey(_ + _)

    val output=wc

    output.saveAsTextFile("output")

    val o=output.collect()

    var s:String="Words:Count \n"
    o.foreach{case(word,count)=>{

      s+=word+" : "+count+"\n"

    }}

  }

}
