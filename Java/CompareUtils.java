package it.chebanca.utils;

import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpression;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.w3c.dom.ls.DOMImplementationLS;
import org.w3c.dom.ls.LSSerializer;
import org.xml.sax.SAXException;

public class CompareUtils {
	
	Map<String, String> expressions = new HashMap<String,String>();

	public boolean compareXML(String inputFile, String masterFile) throws ParserConfigurationException, SAXException, IOException, XPathExpressionException{

		File f1 = new File(masterFile);
		File f2 = new File(inputFile);
		
		String against = linearizeXML(getStringFromFile(f1));
		String actualResponse = linearizeXML(getStringFromFile(f2));
		
		DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
		DocumentBuilder builder = factory.newDocumentBuilder();
		Document doc = builder.parse(new ByteArrayInputStream(against.getBytes()));
		
		Document docRes = builder.parse(new ByteArrayInputStream(actualResponse.getBytes()));
		
		System.out.println("1: "+getStringFromDoc(doc));
		removeEmptyTags(doc);
		System.out.println("2: "+getStringFromDoc(doc));
		buildExpressionString(doc, new StringBuffer());
		System.out.println("3: "+getStringFromDoc(doc));
			
		XPathFactory xPathfactory = XPathFactory.newInstance();
		XPath xpath = xPathfactory.newXPath();
		
		ArrayList<String> errors = new ArrayList<String>();
		for(String exprString: expressions.keySet()){
			XPathExpression expr = xpath.compile(exprString);
			Object res = expr.evaluate(docRes, XPathConstants.STRING);
			if(!((String)res).equals(expressions.get(exprString))) {
				errors.add("Campo " + exprString.replace("/text()", "") + " non presente o non corretto; valore atteso: "+expressions.get(exprString));
				System.out.println(errors.get(errors.size()-1));
			}
		}
		if(errors.size()>0) return false;
		return true;
	}
	
	private void buildExpressionString(Node item, StringBuffer str) {

		if(isLeaf(item)) {
			getParentPath(item, str);
			str.append("/"+item.getNodeName());
			str.append("/text()");
			expressions.put(str.toString(), item.getTextContent());
			System.out.println(str.toString());
			str.delete(0, str.length());
		}
		NodeList nl = item.getChildNodes();
		for(int i = 0;i<nl.getLength();i++){
			Node elem = nl.item(i);
			if(elem.getNodeType() != Node.TEXT_NODE) buildExpressionString(elem, str);			
		}
	}
	
	private void getParentPath(Node item, StringBuffer str) {
		if(!item.getOwnerDocument().equals(item.getParentNode())){
			getParentPath(item.getParentNode(), str);
		}
		if(!item.getOwnerDocument().equals(item.getParentNode())) str.append("/"+item.getParentNode().getNodeName());
	}

	/**
	 * Verify if the node is a leaf
	 */
	private boolean isLeaf(Node node){

		if(node.getChildNodes().getLength()==0 || (node.getChildNodes().getLength()==1 && node.getChildNodes().item(0).getNodeType() == Node.TEXT_NODE)) return true;
		for(int i=0; i<node.getChildNodes().getLength();i++){
			Node n = node.getChildNodes().item(i);
			if(!isEmptyTag(n) && n.getNodeType() == Node.ELEMENT_NODE) return false; 
		}
		return true;
	}

	/**
	 * Remove all empty text tags from node tree.
	 * @param node
	 */
	private void removeEmptyTags(Node node){
		if ( node.hasChildNodes() ){
			NodeList nl = node.getChildNodes();
			for(int i=0;i<nl.getLength();i++){
				Node tmp = nl.item(i);
//				System.out.println("N: "+tmp.getNodeName());
				if ( isEmptyTag(tmp) ){
					i=0;	//restart loop
					node.removeChild(tmp);
					nl = node.getChildNodes();
				}else{
//					System.out.println(node.getNodeName() +"__"+node.getNodeValue());
					removeEmptyTags(tmp);
				}
			}
		}
	}
	
	/**
	 * Check if text tag is empty.  
	 * @param node
	 * @return true if node is text tag, containing only space chars.
	 */
	private boolean isEmptyTag(Node node){
		if ( node.getNodeValue()==null) return false;
		if ( node.hasAttributes() ) return false;
		if ( node.hasChildNodes() ) return false;
		String s = node.getNodeValue();
		for(int i=0;i<s.length();i++){
			char ch = s.charAt(i);
			if ( !isEmptyChar(ch) ) return false;
		}
		return true;
	}
	
	
	private boolean isEmptyChar(char ch){
		if ( Character.isWhitespace(ch) ) return true;
		if ( Character.isSpaceChar(ch) ) return true;
		if ( ch == ' ' ) return true;
		if ( ch=='\b' || ch=='\t' || ch=='\n' || ch=='\f' || ch=='\r' ) return true;
		return false;
	}


	private String getStringFromDoc(org.w3c.dom.Document doc)    {
	    DOMImplementationLS domImplementation = (DOMImplementationLS) doc.getImplementation();
	    LSSerializer lsSerializer = domImplementation.createLSSerializer();
	    return lsSerializer.writeToString(doc);   
	}
	
	private String getStringFromFile(File f) throws IOException{
		BufferedReader br = new BufferedReader(new FileReader(f));
		
		String line = "";
		String res = "";
		while((line = br.readLine())!=null){
			res+=line;
		}
		return res;
	}
	
	private String linearizeXML(String input){
		
		String output ="";
		
		output = input.replaceAll(">[\\s]*<", "><");
//		System.out.println(output);
		return output;
	}

}
