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
		
		
		if(g_length>1){
			int midpoint=g_length/2;
			int left[]=new int[midpoint];
			int right[]=new int[g_length-midpoint];
			
			for(int i=0;i<left.length;i++){
				left[i]=givenArray[i];
				//System.out.print(left[i]+" ");
			}
			//System.out.print("\n");
			for(int j=0;j<right.length;j++){
				right[j]=givenArray[midpoint+j];
				//System.out.print(right[j]+" ");
			}
			//System.out.print("\n");System.out.print("\n");
			mergeSort(left);
			mergeSort(right);
			merge(left,right,givenArray);
		}
		
	}
	
	//quick sort. worse case O(n2), average O(nlogn)
	public static void quickSort(int start, int end,int[] givenArray){
		if(start<end){
			int p_index=partition(start,end,givenArray);
			//System.out.println(p_index);
			quickSort(start,p_index-1,givenArray);
			quickSort(p_index+1,end,givenArray);
		}
	}
	
	public static int partition(int start, int end, int[] givenArray){
		int p_index=start;
		int pivot=givenArray[end];
		int temp=0;
		
		for(int i=start;i<end;i++){
			if(givenArray[i]<=pivot){
				temp=givenArray[p_index];
				givenArray[p_index]=givenArray[i];
				givenArray[i]=temp;
				p_index++;
				
			}
		}
		
		int ntemp=givenArray[p_index];
		givenArray[p_index]=pivot;
		givenArray[end]=ntemp;
		return p_index;
		
	}
	//selection sort.average O(n^2)
	public static void selectionSort(int[] givenArray){
		int g_length=givenArray.length;
		
		for(int i=0;i<g_length-1;i++){
			int smallest=i;
			for(int j=i+1;j<g_length;j++){
				if(givenArray[smallest]>givenArray[j]){
					smallest=j;
				}
			}
			int temp=givenArray[smallest];
			givenArray[smallest]=givenArray[i];
			givenArray[i]=temp;
		}
		
	}
	
	//insertion sort. Average case O(n^2)
	public static void insertionSort(int[] givenArray){
		int g_length=givenArray.length;
		int temp;
		
		for(int i=0;i<g_length;i++){
			while(i>0){
				if(givenArray[i]>givenArray[i-1]){
					temp=givenArray[i];
					givenArray[i]=givenArray[i-1];
					givenArray[i-1]=temp;
					i--;
				}
			}
		}
	}

	public static void main(String[] args) {
		int array_length=10;
//	    int[] numberArray = new int[array_length];
//	    
//		Random rn = new Random();
//		for(int i=0;i<array_length;i++){
//			int answer = rn.nextInt(100 - 1 + 1) + 1;
//			numberArray[i] = answer;
//		}
		
		int[] numberArray={4,6,2,9,1,10,3,8,5,7};
		System.out.print("Original: ");
		for(int i=0;i<numberArray.length;i++){
			System.out.print(numberArray[i] + " ");
		}
		
		
//		System.out.print("\n");
//		//bubblesort
//		bubbleSort(numberArray);
//		System.out.print("Bubble sort: ");
//		for(int i=0;i<array_length;i++){
//			System.out.print(numberArray[i] + " ");
//		}
//		
//		System.out.print("\n");
//		//mergesort
//		mergeSort(numberArray);
//		System.out.print("Merge sort: ");
//		for(int i=0;i<numberArray.length;i++){
//			System.out.print(numberArray[i] + " ");
//		}
		
//		System.out.print("\n");
//		//selectionsort
//		selectionSort(numberArray);
//		System.out.print("Selection sort: ");
//		for(int i=0;i<array_length;i++){
//			System.out.print(numberArray[i] + " ");
//		}
		
//		System.out.print("\n");
//		//insertionsort
//		selectionSort(numberArray);
//		System.out.print("Insertion sort: ");
//		for(int i=0;i<array_length;i++){
//			System.out.print(numberArray[i] + " ");
//		}
//		
		System.out.print("\n");
		//quicksort
		quickSort(0,numberArray.length-1,numberArray);
		System.out.print("Quick sort: ");
		for(int i=0;i<array_length;i++){
			System.out.print(numberArray[i] + " ");
		}
		
		
	}

}
