# Graph  program makefile


JAVAC=/usr/bin/javac

.SUFFIXES: .java .class

.java.class:
	$(JAVAC) $<

classes: DataSet.class \
         Path.class Edge.class Vertex.class GraphException.class  \
         Graph.class GraphExperiment.class



default: $(CLASSES)

clean:
	rm *.class


