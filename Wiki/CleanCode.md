# Clean Code
#### Book Summary

## Chapter 1: Clean Code
Always convey your concerns regarding the time needed to your managers & marketers to avoid bad code. Don’t be shy, to tell the truth, most people want to hear the truth even when they don’t like it and most importantly they want good code. It is unprofessional for engineers to bend to the will of the managers who don’t understand the risks of making messes like doctors don’t. Clean code is readable, extendable by other developers, has unit tests, and does what you expect from it. Always remember while writing the code that you are an author and the author must create ease for their readers, the time ratio between writing and reading the code is 10:1. We are constantly reading old code as part of an effort to write new code. Making a code easier to read actually makes it easier to write.
Boy Scout Rule: “Leave the code cleaner than you found it”
Cleaning doesn’t have to include big changes, you can start by renaming variable names, breaking larger functions into smaller functions, and eliminating duplicate lines.
## Chapter 2: Meaningful Name
Clarity is King, take care of your names & change them whenever you find a better one. The name should reveal its intent & usage, if you need to add a comment for the name then you’ve not named it correctly, names should be pronounceable, searchable. Beware of using a name that varies in small ways i.e XYZCollectionForYou & XYZCollectionInYou, using inconsistent spelling is disinformation.
Avoid using noise words (words that are different but don’t provide any information), the word variable should not be in the variable name.
A truly awful example of variable names is using small L or capital O. Also single letter or numeric names aren’t searchable. Longer names trump the shorter ones and searchable names trump simple constant names. Single-letter names should be used only in the local context.
Implicitly of the code is the degree to which context isn’t visible in the code itself.
Don’t use data type names with variables that don’t belong to that group, i.e don’t name a collection list if it isn’t a list type. Distinguish names in such a way that the reader knows what differences they offer. The length of the variable name should correspond to the size of its scope. If language enforces types then don’t use type in variable names. Include problem & solution domain words in your names.
Interfaces and implementation, use some prefix with interface or implementation to have the distinction between both.
Mental Mapping should be avoided so that users don’t have to map your variable names with terms they already know or map your single-letter variable to their terms. Concerning the scope of the loop, you can use i, j, or k for counters as its tradition. 
Class Name: Class name should be noun phrases instead of verbs
Method Name: Method names should contain verbs, should have prefix/suffix when needed. While using constructor overloading, use static factory methods that describe arguments. Say what you mean and mean what you say. Function names should stand alone. Don’t use cultural terms or slang names i.e eatMyShorts for abortGame name.
Pick one word for one concept & stick with it. i.e don’t have get, fetch & retrieve different names for the same method stick with one convention. Don’t add more context to the name than necessary.
Shorter names are better than long ones as they are clear, don’t add more context than necessary.
## Chapter 3: Functions
The function should communicate its intent and the type of program it lives in. Should be small, tell its story & do only one task. The function shouldn’t be 100 lines big and the lines shouldn’t be 150 characters long, try to limit your function to 20 lines. A function is doing more than 1 thing if another function can be extracted from it.
The Stepdown rule: Every function should be followed by those with the next level of abstraction so that it can be read in descending levels of abstractions.
The function shouldn’t hold nested structures, call another function from If statement inside a function, if there are more than two statements in its body. A function doing more than 1 thing if you can extract another function from it. All the statements in function should be at the same level of abstraction. The function should be written in the “Top to Bottom” pattern, dependency function should be written below the caller. Try to avoid switch statements by using Abstract factory. A descriptive long name is better than a short vague name.
Switch statements do N things so try to bury them in lower-order so that they are not repeated.
Arguments
Introducing arguments brings another distraction in the story so try to avoid it. One argument is the next best thing to no arguments. The function should accept param to apply some transformation & then return it or make some decision based upon passed param. Arguments force readers to remember the context and are harder with testing perspective. Output arguments are even harder than input arguments.
Passing Flag to function means it does more than one thing so avoid it.
If you need to pass more than two or three params to a function consider packing those inside a struct or class.
Function & argument should form a pair of verb & noun
Side Effects functions shouldn’t have any side effects, should do only what its name says.
Anything that forces you to check the function header is double-take, should be avoided.
Command Query Separation Function should either do something or return something, not both.
The function should raise exceptions instead of returning error codes. Function with try/catch should contain only that block, nothing should come after that block in that function body.
Chapter 4: Comments
“Don’t comment bad code, rewrite it” 
Nothing can be more damaging than old comments in code that spread lies. Comments are considered necessary evils, used as compensation for our failure to express ourselves in code. Truth can only be found in one place, that is the code itself not in the comments because code evolves & changes over time but comments don’t.
Think again about restructuring the code if comments are required and their use is not a cause for celebration. Instead of writing comments to explain the code, better clean the code.
Comments don’t make up for bad code: Clear and expressive code is far better than cluttered and complex code with a lot of comments.
Explain yourself in the code: 
Good Comments
Good comments are those which aren’t written. Copyright & authorship can be written in comments. 
Comments before complex logic or regex explaining the intent are useful, sometimes an explanation regarding why a task is being done this particular way. Comments should be used to explain the code that doesn’t explain itself.
It is useful to write warning comments about certain consequences & TODO comments for pending tasks.
Bad Comments
If you’ve to spend time deciding it is the best possible comment then revisit your code. Any comment that forces you to look at another module to understand its intent is a failure. Comment should be precise than code, functions should have comments/doc-string only when needed. If the comment is restating the obvious then it is a noisy comment. Don’t write comment-oriented code, write comments after writing your logic if necessary. Don’t write position marker comments to indicate the start of a sub-category of functions, use few not many if required. 
If you feel the urge to write a closing bracket comment then you should consider breaking your function into sub-functions. Don’t leave commented-out code, others will feel it's too important to delete & it will stay there forever. Comment should stay closer to the line of code it was added for. 
## Chapter 5: Formatting
Code formatting is too important to ignore, first should choose a set of rules that should govern the code format & should be followed consistently. When someone looks at our code they should be impressed with neatness, consistency, orderliness, and sense with the perception of professional being at work.
Purpose of Formatting: The functionality that you’ve developed today might change in the next release but the readability will have a profound & everlasting impact on your code. Your style & discipline survives even though code might not.
Vertical Formatting Aim for smaller files as they are easier to maintain.
Newspaper Metaphor Details should increase as we move downward as found in newspapers, code should be divided into small groups of line-like paragraphs.
Vertical Openness b/w Concepts Group of expressions representing a thought should be separated with a blank line.
Vertical Density That lines that are related should vertically dense.
Vertical Distance: Concepts that are related to each other should be kept vertically close to each other, so related concepts should be kept in one file when possible.
Variable Declarations: Variables should be declared close to their usage and loop variables should be declared within the loop statement.
Instance Variables: should be declared at the top of the class. Instance variable place should be consistent so everyone knows where to find it when needed.
Dependent Functions: If one function call another, they should be placed close to each other, the caller should be above the callee if possible.
Conceptual Affinity: Collection of related concepts should be close, stronger the association lesser the distance. Affinity can be because of functionality performed by functions or naming conventions used.
Horizontal Formatting: The line shouldn’t be over 120 characters long, lesser the better.
Horizontal Openness: Spaces should indicate closeness, the assignment operator should have space because it shows two different operands, while function calls should not have because they represent the same thing.
Indentation: Each source represents multiple scopes, i.e on class level, function level, and block level, all these scopes should be properly indented. Methods in class should be indented one level to the left and blocks should be one level to the containing methods.
Team Rules: Every programmer has his set of favorite rules when you work in a team then team rules should be followed so that project is built with symmetry. 
