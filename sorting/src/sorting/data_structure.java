package sorting;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.Map;
import java.util.Random;
import java.util.Set;


public class data_structure {

	public static void main(String[] args) {
		
		//arrayList,linkedlist
		ArrayList alist = new ArrayList();
		Random rn = new Random();
		
		for(int i=0;i<10;i++){
			
			int answer = rn.nextInt(100 - 1 + 1) + 1;
			alist.add(answer);
		}
		System.out.println("Arraylist:" + alist + "\n");
		
		
		//hashmap
		HashMap hm = new HashMap();
		hm.put("tarik", new Double(200.56));
		hm.put("Ratul", new Double(2323.64));
		hm.put("Tahmid", new Double(345.56));
		hm.put("Hadi", new Double(234324.67));
		hm.put("Dora", new Double(23432.56));
		hm.put("Hamza", new Double(23453.56));
		hm.put("Camilo", new Double(76424.04));
		
		Set set = hm.entrySet();
		Iterator iter = set.iterator();
		
		while(iter.hasNext()){
			Map.Entry map = (Map.Entry)iter.next();
			System.out.println("Name: " + map.getKey() + " | " + "Balance: " + map.getValue() + "\n");
		}

	}

}
