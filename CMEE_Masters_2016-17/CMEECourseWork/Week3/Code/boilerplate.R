# A simple R function - prints the type of 2 variables.
# Functions accept arguments and return values.

MyFunction <- function(Arg1, Arg2){
# 'MyFunction' is a function with 2 arguments.
    
  # Statements involving Arg1, Arg2:
  print(paste("Argument", as.character(Arg1), "is a", class(Arg1))) # print Arg1's type
  print(paste("Argument", as.character(Arg2), "is a", class(Arg2))) # print Arg2's type
  # 'paste()' concatenates strings (concatenates vectors after converting to characters).
  # Here, concatenates 4 objects. 'as.character()' converts 'ArgX' to object of type character. 'class()' IDs ArgX's variable type.
  
  return (c(Arg1, Arg2)) #this is optional, but very useful
  # 'c()' combines values into a vector/list.
  # 'return' so this vector can be passed to other functions.
}
# Curly brackets mark where the function starts/ends.

MyFunction(1,2) # Test the function
MyFunction("Riki","Tiki") # A different test
