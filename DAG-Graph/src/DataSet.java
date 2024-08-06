import java.util.Scanner;
import java.util.Arrays;   
import java.util.ArrayList;  
import java.io.File;  // Import the File class
import java.io.IOException;  // Import the IOException class to handle errors 
import java.io.FileWriter;

public class DataSet{  
    
    //METHOD TO CREATE A UNIQUE EDGE BETWEEN NODES 
    public static String EdgeCreate(int max){
	int v1 = (int)Math.floor(Math.random() * (max - 0 + 1) + 0);
	int v2 = (int)Math.floor(Math.random() * (max - 0 + 1) + 0); 
	String Edge;
	     
	if( v1 != v2) { 
	   Edge = "Node"+v1+" "+"Node"+v2; 
	   return Edge; 
	   } 
	     
	else{ 
	   return EdgeCreate(max); 
	   }
     }

   
   public static void main( String [ ] args )
    { 
   //-------------------------------------------------//  
     //1.GET PARAMETERS # OF VERTICES AND EDGES
     Scanner input = new Scanner(System.in);
     System.out.print("Enter number of Vertices: ");
     int numV = input.nextInt(); // NUMBER OF VERTICES 
     
     System.out.print("Enter number of Edges: ");
     int numE = input.nextInt(); //NUMBER OF EDGES 
   //-------------------------------------------------//
     //2. STORE VERTICES IN ARRAY
     ArrayList<String> arrV = new ArrayList<String>(); //VERTICES ARRAY
     
     for (int i = 0; i < numV; i++) {  
       arrV.add("Node"+i); // ADD VERTICES INTO ARRAY
       }  
   //-------------------------------------------------//
     //3.CREATE EDGE BETWEEN VERTICES AND STORE WITHIN EDGE ARRAY
      String EdgeCost; 
      ArrayList<String> arrE = new ArrayList<String>(); //ARRAY OF EDGES
      String E;
      
      for (int i = 0; i < numE + 1 ; i++) {  
       E = EdgeCreate(numV); 
       if (arrE.contains(E)){
         E = EdgeCreate(numV);
        } 
       else{ 
        arrE.add(E);
       } 
      }   
   //-------------------------------------------------//
    //4. CREATE EDGES WITH COST   
      ArrayList<String> arrEC = new ArrayList<String>(); //ARRAY OF EDGES WITH COST
      for (int i = 0; i < arrE.size(); i++) {
      EdgeCost = arrE.get(i)+" "+(int)Math.floor(Math.random() * (10 - 1 + 1) + 1); 
      arrEC.add(EdgeCost);
    }  
    
    for (int i = 0; i < arrEC.size(); i++) {
      System.out.println(arrEC.get(i));
    }
   //------------------------------------------------// 
    //5. CREATE A DATASET TEXT FILE
    try {
      File myObj = new File("Graph.txt");
      FileWriter myWriter = new FileWriter("Graph.txt"); 
      for (int i = 0; i < arrEC.size(); i++) {
       myWriter.write(arrEC.get(i)+"\n");
       }
      myWriter.close();
      System.out.println("Successfully wrote to the file.");
     } 
    catch (IOException e) {
      System.out.println("An error occurred.");
      e.printStackTrace();
    }
   //------------------------------------------------//
    //6. CREATE GRAPH AND RUN DJIKSTRA ALGORITHM 
    
        
      
       
    /* int min = 50; // Minimum value of range
      int max = 100; // Maximum value of range
      // Print the min and max  
      System.out.println("Random value in int from "+ min + " to " + max + ":");
      // Generate random int value from min to max
      int random_int = (int)Math.floor(Math.random() * (max - min + 1) + min);
      // Printing the generated random numbers
      System.out.println(random_int); */
    }
}
