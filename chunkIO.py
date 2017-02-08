from game import Game
from corrupted_chess_file_error import *
from player import Player
from piece import Piece
from board import Board

class ChunkIO(object):

    def load_game(self, input):

        '''
        @note:This is the game object this method will fill with data. The object
               is returned when the END chunk is reached.
        '''
        def PLR(self, teksti, pituus):
                color = self.read_fully(1, teksti)
                color = "".join(color)
                pituus -= 1
                if color == "M":
                    color = Player.BLACK
                elif color == "V":
                    color = Player.WHITE
                else:
                    raise CorruptedChessFileError("Pelaajan tulee olla valkoinen tai musta!")
                name = self.read_fully(self.read_fully(self.read_fully(1, teksti), teksti), teksti)
                name = "".join(name)
                pituus -= len(name)
                
                if name == "":
                    raise CorruptedChessFileError("Nimi ei voi olla tyhja.")
                
                nappulat = self.read_fully(len(pituus), teksti)
                nappulat = "".join(nappulat)
                Nappula(nappulat, self, len(nappulat))
                return Player(name, color)
            
        def Nappula(self, teksti, omistaja, size):
            while size > 0:
                nappula = self.extract_chunk_name(teksti)
                tyyppi = self.read_fully(1, nappula)
                piece = Piece(omistaja, tyyppi)
                column = self.read_fully(1, teksti)
                row = self.read_fully(1, nappula)
                lauta.set_piece(piece, lauta.column_char_to_integer(column), lauta.row_char_to_integer(row))
                size -= 3
                

        self.game = Game()

        try:

            # Read the file header and the save date
            
            header = self.read_fully(8, input)
            date = self.read_fully(8, input)
            

            # Process the data we just read.
            # NOTE: To test the line below you must test the class once with a broken header
            
            header = ''.join(header)
            date = ''.join(date)
            if not str(header).startswith("SHAKKI"):
                raise CorruptedChessFileError("Unknown file type")
            tunniste = self.read_fully(5, input)
            tunniste = ''.join(tunniste)
            print(tunniste)
            blokki = self.read_fully(self.extract_chunk_size(tunniste), input)
            print(blokki)
            blokki = ''.join(blokki)
            print(blokki)
            playercount = 0
            lauta = Board()
            while self.extract_chunk_name(tunniste) != "END" and self.extract_chunk_size(tunniste) != 0:
                
                if self.extract_chunk_name(tunniste) == "PLR" and playercount == 0:
                    print(tunniste)
                    pelaaja1 = PLR(blokki, self.extract_chunk_size(tunniste))
                    playercount += 1
                   
                    
                elif self.extract_chunk_name(blokki) == "PLR" and playercount == 1:
                    
                    pelaaja2 = PLR(blokki, self.extract_chunk_size(tunniste)) 
                    playercount += 2
                    
                    
                if playercount > 2:
                    
                    raise CorruptedChessFileError("Pelaajia ei voi olla yli kahta!")
                
                tunniste = self.read_fully(5, input)
                tunniste = ''.join(tunniste)
                blokki = self.read_fully(self.extract_chunk_size(tunniste), input)
                blokki = ''.join(blokki)
            
            if playercount != 2:
                
                raise CorruptedChessFileError("Pelaajia on oltava 2!")

            # The version information and the date are not used in this
            # exercise
            
            # *************************************************************         #
            # EXERCISE
            #
            # ADD CODE HERE FOR READING THE
            # DATA FOLLOWING THE MAIN HEADERS
            #
            #
            # *************************************************************
            
                    
                    
                
                
            
            # If we reach this point the Game-object should now have the proper players and
            # a fully set up chess board. Therefore we might as well return it.
            
            return self.game

        except OSError:

            # To test this part the stream would have to cause an
            # OSException. That's a bit complicated to test. Therefore we have
            # given you a "secret tool", class BrokenReader, which will throw
            # an OSException at a requested position in the stream.
            # Throw the exception inside any chunk, but not in the chunk header.            
            raise CorruptedChessFileError("Reading the chess data failed 1.")




    # HELPER METHODS -------------------------------------------------------



    def extract_chunk_size(self, chunk_header):
        '''
        Given a chunk header (an array of 5 chars) will return the size of this
        chunks data.
        
        @param chunk_header:
                   a chunk header to process (str)
        @return: the size (int) of this chunks data
        '''

        
        # subtracting the ascii value of the character 0 from
        # a character containing a number will return the
        # number itself

        asd = int( ''.join( chunk_header[3:5] ) )
        print(asd)
        return asd

        '''
        Given a chunk header (an array of 5 chars) will return the name of this
        chunk as a 3-letter String.
        
        @param chunk_header:
                   a chunk header to process
        @return: the name of this chunk
        '''
    def extract_chunk_name(self, chunk_header):
        return ''.join( chunk_header[0:3] )
    

    def read_fully(self, count, input):
        '''
        The read-method of the Reader class will occasionally read only part of
        the characters that were requested. This method will repeatedly call read
        to completely fill the given buffer. The size of the buffer tells the
        algorithm how many bytes should be read.
        
        @param count:
                   How many characters are read
        @param input:
                   The character stream to read from
        @raises: OSError
        @raises: CorruptedChessFileError
        '''
        read_chars = input.read( count )
        
        # If the file end is reached before the buffer is filled
        # an exception is thrown.    
        if len(read_chars) != count:
                raise CorruptedChessFileError("Unexpected end of file.")

        return list(read_chars)
