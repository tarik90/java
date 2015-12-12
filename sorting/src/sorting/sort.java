package sorting;

import java.util.Random;

public class sort {
	
	int[] numberArray = new int[10];
	
	//bubblesort. best case O(n).worse case O(n^2)
	public static void bubbleSort(int[] givenArray){
		int temp;
		for(int i=0;i<givenArray.length-1;i++){
			for(int j=0;j<givenArray.length-1;j++){
				if(givenArray[j]>givenArray[j+1]){
					temp=givenArray[j];
					givenArray[j]=givenArray[j+1];
					givenArray[j+1]=temp;
				}
			}
		}
	}
	
	//mergesort. worse case O(nlogon)
	public static void merge(int[] left,int[] right, int[] givenArray){
		int l_length=left.length;
		int r_length=right.length;
		int g_length=givenArray.length;
		int i=0,j=0,k=0;
		while(i<l_length && j<r_length && k<g_length){
			if(left[i]>right[j]){
				givenArray[k]=right[j];
				j++;
				k++;
			}
			else if(right[j]>left[i]){
				givenArray[k]=left[i];
				i++;
				k++;
			}
		}
	}
	
	
	public static void mergeSort(int[] givenArray){
		int g_length=givenArray.length;
		
		
		if(g_length>2){
			int midpoint=g_length/2;
			int left[]=new int[midpoint];
			int right[]=new int[g_length-midpoint];
			
			for(int i=0;i<midpoint;i++){
				left[i]=givenArray[i];
			}
			
			for(int j=0;j<g_length-midpoint;j++){
				right[j]=givenArray[midpoint+j];
			}
			
			mergeSort(left);
			mergeSort(right);
			merge(left,right,givenArray);
		}
		
	}

	public static void main(String[] args) {
	    int[] numberArray = new int[10];
		Random rn = new Random();
		for(int i=0;i<10;i++){
			int answer = rn.nextInt(100 - 1 + 1) + 1;
			numberArray[i] = answer;
		}
		System.out.print("Original: ");
		for(int i=0;i<10;i++){
			System.out.print(numberArray[i] + " ");
		}
		
		System.out.print("\n");
		
		//bubblesort
		bubbleSort(numberArray);
		System.out.print("Bubble sort: ");
		for(int i=0;i<10;i++){
			System.out.print(numberArray[i] + " ");
		}
		
		System.out.print("\n");
		
		//mergesort
		mergeSort(numberArray);
		System.out.print("Merge sort: ");
		for(int i=0;i<10;i++){
			System.out.print(numberArray[i] + " ");
		}
		
		
	}

}
