CREATE TABLE [dbo].[regtable]
(
	[uName] VARCHAR(50) NOT NULL, 
    [gender] VARCHAR(50) NOT NULL, 
    [city] VARCHAR(50) NOT NULL, 
    [contact] VARCHAR(50) NOT NULL, 
    [email] VARCHAR(50) NOT NULL, 
    CONSTRAINT [PK_regtable] PRIMARY KEY ([email]) 
)
