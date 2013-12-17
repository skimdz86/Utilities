package it.mdz.xml;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.StringWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.w3c.dom.Text;

public class XMLCompare
{

    /**
	 * @author MDZ
     * @param args
     * @throws Exception 
     */
    public static void main(String[] args) throws Exception
    {
        // TODO Auto-generated method stub
    	XMLCompare compare = new XMLCompare();
//    	String str = compare.reorderXML("C:\\mapping.xml", "name");
//    	compare.writeFile(str, "C:\\tmp\\reordered.xml");
//    	System.out.println(compare.compare("C:\\mapping.xml", "C:\\mapping2.xml", "name"));
    	
    	if(args.length==0) {
    		System.out.println("Passare gli argomenti necessari: XMLCompare [compare/reorder] {other args}");
    		return;
    	}
    	
    	if("compare".equals(args[0])){
    		if(args.length<4) {
        		System.out.println("Passare gli argomenti necessari: XMLCompare [compare] [inputFilePath1] [inputFilePath2] [orderAttribute]");
        		return;
        	}
    		System.out.println(compare.compare(args[1], args[2], args[3]));
    	}
    	else if("reorder".equals(args[0])){
    		if(args.length<4) {
        		System.out.println("Passare gli argomenti necessari: XMLCompare [compare] [inputFilePath] [orderAttribute] [outputFilePath]");
        		return;
        	}
    		String str = compare.reorderXML(args[1], args[2]);
    		compare.writeFile(str, args[3]);
    	}
    	
    	
    }

    /**
     * Reorder xml tags based on the value of the attribute specified
     * @param fileName Full name of the input file
     * @param keyOrderAttr Name of the attribute for the ordering
     * */
    public String reorderXML(String fileName, String keyOrderAttr) throws Exception{
    	
    	HashMap<String, Element> nodeMap = new HashMap<String, Element>();
    	List<String> nodeNames = new ArrayList<String>();
    	
    	File file = new File(fileName);
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        DocumentBuilder db = dbf.newDocumentBuilder();
        Document doc = db.parse(file);
        doc.getDocumentElement().normalize();
        String root = doc.getDocumentElement().getNodeName();
        NodeList serviceNodes = getOnlyStructureChildNodes(doc.getDocumentElement());
        
        
        for(int j=0;j<serviceNodes.getLength();j++){
        	Element elem = (Element)serviceNodes.item(j);
        	String orderName = elem.getAttribute(keyOrderAttr);
        	nodeMap.put(orderName, elem);
        	nodeNames.add(orderName);
        }
        
        //SORT
        Collections.sort(nodeNames);
        Document docNew = db.newDocument();
        Element rootElement = docNew.createElement(root);
        for(String s: nodeNames){
        	Node importedNode = docNew.importNode(nodeMap.get(s), true);
        	rootElement.appendChild(docNew.createTextNode("\n  "));
        	rootElement.appendChild(importedNode);
        }
        rootElement.appendChild(docNew.createTextNode("\n"));
        docNew.appendChild(rootElement);
        
        TransformerFactory transFactory = TransformerFactory.newInstance();
        Transformer transformer = transFactory.newTransformer();
        StringWriter buffer = new StringWriter();
        transformer.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "yes");
        transformer.transform(new DOMSource(docNew), new StreamResult(buffer));
        String str = buffer.toString();
        str = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" + str;
        
        return str;
    }
    
    public boolean compare(String filePath1, String filePath2, String keyOrderAttr) throws Exception{
    	String str1 = reorderXML(filePath1, keyOrderAttr);
    	String str2 = reorderXML(filePath2, keyOrderAttr);
    	
    	str1 = str1.replaceAll("\r\n", "");
    	str1 = str1.replaceAll("\n", "");
    	str2 = str2.replaceAll("\r\n", "");
    	str2 = str2.replaceAll("\n", "");
    	    	
    	if(str1.equals(str2)) return true;
    	return false;
    }
    
    public void writeFile(String str, String outputFile){
    	BufferedWriter writer = null;
		try {
			writer = new BufferedWriter(new FileWriter(outputFile));
			writer.write(str);

		} catch (IOException e) {
		} finally {
			try {
				if (writer != null)
					writer.close();
			} catch (IOException e) {
			}
		}
    }
    
    /**
     * Recupera tutti i nodi figli escludendo i nodi di solo testo
     * */
    private static NodeList getOnlyStructureChildNodes(Node parent){
		 NodeList childNodes = parent.getChildNodes();
		 for(int i = 0; i<childNodes.getLength(); i++){
			 if(childNodes.item(i) instanceof Text){
				 parent.removeChild(childNodes.item(i));
			 }
		 }
		 return parent.getChildNodes();
	 }
}
