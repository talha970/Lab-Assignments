package proj;
import java.util.*;
public class myclass {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		int[] arr={1,3,2,1,3};
		HashMap<Integer,Integer> map=new HashMap();
for(int i=0;i<arr.length;i++){
	if(!map.containsKey(arr[i])){
		map.put(arr[i],1);
	}
	else{
		map.put(arr[i],2);
	}
		
}
for (Map.Entry<Integer,Integer> entry : map.entrySet()) {
	  int key = entry.getKey();
	  int value = entry.getValue();
	//  System.out.println(key+" : "+value);
	  // do stuff
	  if(value==1){
		  System.out.println(key);
		  break;
	  }
	}
	}

}
