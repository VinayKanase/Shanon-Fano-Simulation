function shannon_fano(varargin)

    % Set default source
    if nargin == 0
        source = 'EAACAADAACAAADAABDBBCBAE';
    else
        source = varargin{1};
    end

    % Calculate the frequency of each symbol in the source
    symbols = unique(source);
    freq = histc(source, symbols);

    % Sort symbols based on their frequency
    [sortedFreq, sortedIdx] = sort(freq, 'descend');
    sortedSymbols = symbols(sortedIdx);

    % Recursive function to split the list, assign codes, and plot
    function [codes, xPos, yPos] = sf_coding(symbols, freq, x, y, delta_y)
        n = length(symbols);
        if n == 1
            codes = {''};
            text(x, y, [symbols, ' ', num2str(freq)], 'HorizontalAlignment', 'center');
            xPos = x;
            yPos = y;
        else
            total = sum(freq);
            half = total / 2;
            currSum = 0;
            split = 0;
            for i = 1:n
                currSum = currSum + freq(i);
                if currSum >= half
                    split = i;
                    break;
                end
            end

            % Left branch (0)
            leftDelta = delta_y * split / n;
            [codes1, xPos1, yPos1] = sf_coding(symbols(1:split), freq(1:split), x-1, y + leftDelta/2, leftDelta);

            % Right branch (1)
            rightDelta = delta_y * (n - split) / n;
            [codes2, xPos2, yPos2] = sf_coding(symbols(split+1:end), freq(split+1:end), x-1, y - rightDelta/2, rightDelta);

            % Draw lines
            line([x, xPos1], [y, yPos1], 'Color', 'k');
            line([x, xPos2], [y, yPos2], 'Color', 'k');
            
            codes1 = strcat('0', codes1);
            codes2 = strcat('1', codes2);
            codes = [codes1 codes2];
            xPos = x;
            yPos = y;
        end
    end

    % Open figure and set axes properties
    figure;
    ax = gca;
    hold on;
    axis off;

    % Generate codes and plot tree
    [~] = sf_coding(sortedSymbols, sortedFreq, 0, 0, length(source));

    title('Shannon-Fano Encoding Tree');
end


%{ 
Probability Table
Symbol	Count	Probability
A	    12	     0.48
B	    4	     0.16
C	    3	     0.12
D	    3	     0.12
E	    2	     0.08

0.16 + 0.12 + 0.12 + 0.08 = 0.48

Symbol	Count	Probability Code
A	    12	     0.48       0

B	    4	     0.16       1
C	    3	     0.12       1
D	    3	     0.12       1
E	    2	     0.08       1


0.16 + 0.12 = 0.28
0.12 + 0.08 = 0.20

Symbol	Count	Probability Code
A	    12	     0.48       0

B	    4	     0.16       1 0 
C	    3	     0.12       1 0

D	    3	     0.12       1 1
E	    2	     0.08       1 1

Final Codes
Symbol	Count	Probability	Code
A	    12	    0.48	    0

B	    4	    0.16	    1 0 0

C	    3	    012	        1 0 1

D	    3	    0.12	    1 1 0

E	    2	    0.08	    1 1 1

%}