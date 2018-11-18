import pandas as pd


classes_data = pd.read_csv('classes.csv')

#Create Model Class

def try_catch(type, numTabs, f):
    #write try block
    if not type == 2:
        for i in range(numTabs):
                f.write("\t")
    if type == 0:
        f.write("try {\n") 
    elif type == 1:
        f.write("} catch (SQLException excep) {\n\n")
        for i in range(numTabs):
            f.write("\t")
        f.write("}")
    elif type == 2:
        f.write(" finally {\n")

convert_type = {'int_primary_key': 'int'}

def create_parameter_list(types, names, f):
    f.write("(")
    for t in range(len(types)):
        if types[t] in convert_type:
            if t == len(types) - 1:
                f.write(convert_type[t] + " " + names[t] + ", ")
            else:
                f.write(convert_type[t] + " " + names[t])
        
        if t == len(types) - 1:
            f.write(types[t] + " " + names[t])
        else:
            f.write(types[t] + " " + names[t] + ",")
    
    f.write(") {")

def create_model_class():
    index = list(classes_data.index.values)
    
    file = "/Users/vishalchopra/Documents/School/University/Second Year/SE 2203/Assignment 3/aoudaiTravel/src/iTravel/"
    
    sql_data_types = {'String': 'CHAR(' + str(15) + ') NOT NULL', 'int_primary_key': 'INT NOT NULL PRIMARY KEY', 'int': 'INT', 'double': 'DOUBLE', 'Date': 'DATE'}
    
    for i in index:
        name = classes_data.loc[i, 'Class Name']
        attributeNames = classes_data.loc[i, 'Class Attribute Names'].split("|")
        attributeTypes = classes_data.loc[i, 'Class Attribute Types'].split("|")
        attributeSymbol = classes_data.loc[i, 'Class Attribute Symbol'].split("|")
        
        f = open(file + name + ".java", "w+")
        
        f.write("package iTravel;\n")
        
        f.write("public class " + name + "{\n")
        
        for i in range(len(attributeNames)):
            f.write("\tprivate " + attributeTypes[i] + " " + attributeNames[i] + ";\n")
        
        # Create constructor
        f.write("\n\n")
        
        f.write("\tpublic " + name + "(")
        
        for i in range(len(attributeNames)):
            
            if i == len(attributeNames) - 1:
                f.write(attributeTypes[i] + " " + attributeSymbol[i])
            else:
                f.write(attributeTypes[i] + " " + attributeSymbol[i] + ",")
                
        f.write("){\n")
        
        for i in range(len(attributeNames)):
            if 'PASSWORD' in attributeNames[i].upper():
                f.write("\t\tthis." + attributeNames[i] + "=Integer.toString(" + attributeSymbol[i] + ".hashCode()" + ");\n")
            else:
                f.write("\t\tthis." + attributeNames[i] + "=" + attributeSymbol[i] + ";\n")
                
        f.write("\n\t}\n")
        
        for i in range(len(attributeNames)):
            f.write("\tpublic void set" + attributeNames[i][0].upper() + attributeNames[i][1:] + "(" + attributeTypes[i] + " " + attributeSymbol[i] + "){\n")
            f.write("\t\tthis." + attributeNames[i] + "=" + attributeNames[i] + ";\n")
            f.write("\t}\n")
            
            f.write("\tpublic " + attributeTypes[i] + " get" + attributeNames[i][0].upper() + attributeNames[i][1:] + "(){\n" + "\t\treturn this." + attributeNames[i] + ";\n\t}\n")
        
        f.write("}")
        
        f.close()
        
        f = open(file + name + "Adapter.java", "w+")
        
        #Create Adapter Class
        f.write("package iTravel;\n")
        f.write("import java.sql.Connection;\n")
        f.write("import java.sql.SQLException;\n")
        f.write("import java.sql.Statement;\n")
        f.write("import javafx.collections.FXCollections;")
        f.write("import javafx.collections.ObservableList;")
        
        f.write("public class " + name + "Adapter {\n")
        f.write("\tConnection connection;\n")
        
        f.write("\tpublic " + name + "Adapter(Connection conn, Boolean reset) throws SQLException {\n")
        f.write("\t\tconnection=conn;\n")
        f.write("\t\tif(reset) {\n")
        
        
        f.write("\t\t\tStatement stmt = connection.createStatement();\n")
        
        try_catch(0, 3, f)
        
        for a in range(len(attributeNames)):
            if attributeNames[a].upper() == 'NAME':
                attributeNames[a] = 's' + attributeNames[a][0].upper() + attributeNames[a][1:]
        
        f.write("\t\t\t\tstmt.execute(\"DROP TABLE " + name.upper() + "\");\n")
        
        try_catch(1, 3, f)
        try_catch(2, 3, f)
        
        f.write("\t\t\t\tstmt.execute(\"CREATE TABLE " + name.upper() + " (\"")
        
        
        for i in range(len(attributeTypes)):
            f.write("\n\t\t\t\t\t+")
            if attributeTypes[i] in convert_type:
                if i == len(attributeTypes) - 1:
                    f.write("\"" + convert_type[i].upper() + " " + sql_data_types[attributeTypes[i]] + "\"") 
                else:
                    f.write("\"" + convert_type[i].upper() + " " + sql_data_types[attributeTypes[i]] + ",\"")
            if i == len(attributeTypes) - 1:
                f.write("\"" + attributeNames[i].upper() + " " + sql_data_types[attributeTypes[i]] + "\"")
            else:
                f.write("\"" + attributeNames[i].upper() + " " + sql_data_types[attributeTypes[i]] + ",\"")
        
        f.write("\n\t\t\t\t\t+ \")\");")
        f.write("\n\t\t\t}")
        f.write("\n\t\t}")
        f.write("\n\t}")
        
        f.write("\n\tpublic void insert" + name)
        create_parameter_list(attributeTypes, attributeSymbol, f)
        f.write("\n")
        
        
        try_catch(0, 2, f)
        f.write("\t\t\tStatement stmt = connection.createStatement();\n")
        f.write("\t\t\tString sqlStatement = \"" + "INSERT INTO " + name.upper() + " (")
        
        for a in range(len(attributeNames)):
            if a == len(attributeNames) - 1:
                f.write(attributeNames[a])
            else:
                f.write(attributeNames[a] + ", ")
        
        f.write(") VALUES\" + " + "\"(\'\"")
        
        for a in range(len(attributeSymbol)):
            if (attributeTypes[a] == "String"):
                if a == 0:
                    f.write(" + " + attributeSymbol[a] + " + \"'")
                else:
                    f.write(",'\" + " + attributeSymbol[a] + " + \"'")
            else:
                if a == 0:
                    f.write(" + \"" + attributeSymbol[a] + " + \"")
                else:
                    f.write(",\" + " + attributeSymbol[a] + " + \"")
                    
        
        f.write(")\";\n")
        
        f.write("\t\t\tstmt.execute(sqlStatement);\n");
        
        
        try_catch(1, 2, f)
        
        f.write("\n\t}")
        
        f.write("\n\tpublic ObservableList<" + name + ">" + " get" + name + "s" " throws SQLException {")
        f.write("\n\t\tObservableList<" + name + "> list = FXCollections.observableArrayList();")
        f.write("\n\t\tResultSet rs;")
        
        #Create statement
        f.write("\n\t\tStatement stmt = connection.createStatement();")
        f.write("\n\t\tString sqlStatement=" + "\"" + "SELECT * FROM" + name.upper() + "\"" + ";")
        
        f.write("\n\t\tstmt.execute(sqlStatement);")
        f.write("\n\t\trs = s.getResultSet();")
        
        f.write("\n\t\twhile(rs.next()){")
        f.write("\n\t\t\tlist.add(")
        f.write()
        
        
        f.write("\n}")
        
        f.close()
        
        
create_model_class()
            
            
        

