import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;
import java.util.HashSet;
public class fileNamer{
	public static <T> int find(T[] arr, T item){
		for(int i=0; i<arr.length; i++){
			if(arr[i].equals(item)){
				return i;
			}
		}
		return -1;
	}
	public static boolean isValid(File file, String name, boolean isDest){
		if(file.getName().length()<=5||!file.getName().substring(file.getName().length()-5).equals(".java")||file.isDirectory()){
			return false;
		}
		if(Character.isDigit(file.getName().charAt(0))){
			System.out.println("\nInvalidClassException: "+name+" requires a disallowed class name (first character is digit)\n");
			return false;
		}
		boolean flag=false;
		for(int j=0; j<file.getName().length()-5; j++){
			if(!(Character.isLetterOrDigit(file.getName().charAt(j))||file.getName().charAt(j)=='_'||file.getName().charAt(j)=='$')){
				System.out.println("\nInvalidClassException: "+name+" requires a disallowed class name (uses characters other than 0-9, a-z, A-Z, _ or $)\n");
				flag=true;
				break;
			}
		}
		if(flag){
			return false;
		}
		String[] reserved={"abstract", "assert", "boolean", "break", "byte", "case", "catch", "char", "class", "continue", "const", "default", "do", "double", "else", "enum", "exports", "extends", "final", "finally", "float", "for", "goto", "if", "implements", "import", "instanceof", "int", "interface", "long", "native", "new", "package", "private", "protected", "public", "requires", "return", "short", "static", "strictfp", "super", "switch", "synchronized", "this", "throw", "throws", "transient", "try", "var", "void", "volatile", "while", "true", "false", "null"};
		if(find(reserved, file.getName().substring(0, file.getName().length()-5))>=0){
			System.out.println("\nInvalidClassException: "+name+" requires a disallowed class name (reserved word)\n");
			return false;
		}
		if(file.isHidden()){
			return false;
		}
		if(isDest){
			return true;
		}
		if(!file.canRead()){
			System.out.println("\nIOException: "+name+" not readable\n");
			return false;
		}
		if(!file.canWrite()){
			System.out.println("\nIOException: "+name+" not writable\n");
			return false;
		}
		return true;
	}
	public static void main(String[] args){
		System.out.println("\nDISCLAIMER: For use on a Linux Virtual Machine installed on a Windows computer only, due to issues with case-sensitivity.\n");
		try{
			if(args[0].length()<=5||!args[0].substring(args[0].length()-5).equals(".java")){
				args[0]+=".java";
			}
			if(args[1].length()<=5||!args[1].substring(args[1].length()-5).equals(".java")){
				args[1]+=".java";
			}
			File origin=new File(args[0]), destination=new File(args[1]);
			if(args[1].equalsIgnoreCase(args[0])){
				System.out.println("\nIOException: input and output files ("+args[0]+") are the same (case-insensitive)\n");
				return;
			}
			if(!origin.exists()||find(origin.getAbsoluteFile().getParentFile().list(), origin.getName())==-1){
				System.out.println("\nFileNotFoundException: input file ("+args[0]+") not found (case-sensitive)\nNote: Use a relative or absolute pathname if the file is in another directory.\n");
				return;
			}
			if(!origin.getAbsoluteFile().getParentFile().equals(destination.getAbsoluteFile().getParentFile())){
				System.out.println("\nIOException: input ("+args[0]+") and output files ("+args[1]+") are in different directories.\n");
				return;
			}
			if(origin.isDirectory()){
				System.out.println("\nIOException: input file ("+args[0]+") is a directory\n");
				return;
			}
			if(destination.exists()){
				System.out.println("\nIOException: output file ("+args[1]+") already exists (case-insensitive)\n");
				return;
			}

			if(!isValid(origin, "input file ("+args[0]+")", false)){
				return;
			}
			if(!isValid(destination, "output file ("+args[1]+")", true)){
				return;
			}
			HashSet<File> files=new HashSet<>();
			for(String name: destination.getAbsoluteFile().getParentFile().list()){
				File temp=new File(name);
				if(isValid(temp, temp.getName(), false)){
					files.add(temp);
				}
			}
			files.add(origin);
			String originName=origin.getName().substring(0, origin.getName().length()-5), destinationName=destination.getName().substring(0, destination.getName().length()-5);
			for(File file: files){
				try(Scanner contents=new Scanner(file)){
					String result="";
					boolean edit=false;
					while(contents.hasNextLine()){
						String line=contents.nextLine();
						int ind=0, count=0;
						boolean strMode=false;
						while(ind+originName.length()<=line.length()){
							if(strMode){
								if(line.charAt(ind)=='\\'){
									count++;
								}else if(count==0&&line.charAt(ind)=='"'){
									strMode=false;
								}
								count=0;
							}else if(line.substring(ind, ind+originName.length()).equals(originName)&&!(ind>0&&(Character.isLetterOrDigit(line.charAt(ind-1))||line.charAt(ind-1)=='_'||line.charAt(ind-1)=='$')||ind+originName.length()<line.length()&&(Character.isLetterOrDigit(line.charAt(ind+originName.length()))||line.charAt(ind+originName.length())=='_'||line.charAt(ind+originName.length())=='$'))){
								line=line.substring(0, ind)+destinationName+line.substring(ind+originName.length());
								ind+=destinationName.length()-1;
								edit=true;
							}
							ind++;
						}
						result+=line+"\n";
					}
					if(edit){
						FileWriter writer=new FileWriter(file);
						writer.write(result);
						writer.close();
					}
				}catch(IOException error){
					error.printStackTrace();
					return;
				}
			}
			origin.renameTo(destination);
		}catch(ArrayIndexOutOfBoundsException error){
			System.out.println("\nSyntaxError: "+(args.length==0?"missing arguments":"missing output file name")+"\nSyntax: java fileNamer.java <inputFileName> <outputFileName>\n");
			return;
		}
		System.out.println("\nFiles renamed and edited successfully.\n");
	}
}