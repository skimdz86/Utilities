package utility;

import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.List;

public class JsonConverter {

	public static String objectToJson(Object o) throws NoSuchMethodException, SecurityException, IllegalAccessException, IllegalArgumentException, InvocationTargetException{
		String res = "";
		Field[] fields = o.getClass().getDeclaredFields();
		for(Field f : fields){
			res += "\""+f.getName()+"\":";
			Method getterMethod = o.getClass().getMethod("get"+f.getName().substring(0, 1).toUpperCase()+f.getName().substring(1), new Class[]{});
			Object getResult = getterMethod.invoke(o, new Object[]{});
			String value = getResult!=null?getResult.toString():null;
			res += "\""+value+"\",";
		}
		if(fields.length>0) res = res.substring(0, res.length()-1);//rimuovo ultima virgola
		res = "{"+res+"}";
		return res;
	}
	
	public static String listToJson(List l, String listName) throws NoSuchMethodException, SecurityException, IllegalAccessException, IllegalArgumentException, InvocationTargetException{
		String res = "";
		
		for(int i=0;i<l.size();i++){
			Object o = l.get(i);
			res += objectToJson(o)+",";
		}
		if(l.size()>0) res = res.substring(0, res.length()-1);//rimuovo ultima virgola
		res = "{\""+listName+"\":["+res+"]}";
		return res;
	}
}
