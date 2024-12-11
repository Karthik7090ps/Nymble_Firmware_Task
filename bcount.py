def count_bits_in_paragraph(paragraph):
    ones_count = 0
    zeros_count = 0
    count=0
    
    # Iterate over each character in the paragraph
    for char in paragraph:
        # Convert character to binary representation
        binary_rep = bin(ord(char))[2:]  # bin(ord(char)) gives binary with '0b' prefix, so slice to get the actual binary
        ones_count += binary_rep.count('1')
        zeros_count += binary_rep.count('0')
        count+=1
    
    return ones_count, zeros_count, count

# Example usage
paragraph = """Finance Minister Arun Jaitley Tuesday hit out at former RBI governor Raghuram Rajan for predicting that the next banking crisis would be triggered by MSME lending, saying postmortem is easier than taking action when it was required. Rajan, who had as the chief economist at IMF warned of impending financial crisis of 2008, in a note to a parliamentary committee warned against ambitious credit targets and loan waivers, saying that they could be the sources of next banking crisis. Government should focus on sources of the next crisis, not just the last one. In particular, government should refrain from setting ambitious credit targets or waiving loans. Credit targets are sometimes achieved by abandoning appropriate due diligence, creating the environment for future NPAs," Rajan said in the note." Both MUDRA loans as well as the Kisan Credit Card, while popular, have to be examined more closely for potential credit risk. Rajan, who was RBI governor for three years till September 2016, is currently."""
ones, zeros, count = count_bits_in_paragraph(paragraph)
print(f"Number of 1's: {ones}")
print(f"Number of 0's: {zeros}")
print(f"count{count*8}")
