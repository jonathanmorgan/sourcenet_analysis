from __future__ import unicode_literals
from __future__ import division

'''
Copyright 2016 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/sourcenet_analysis.

sourcenet_analysis is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

sourcenet_analysis is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/sourcenet. If not, see http://www.gnu.org/licenses/.
'''

# python built-in libraries
import hashlib

# python package imports
import six

# django imports
from django.contrib.auth.models import User

# python_utilities
from python_utilities.exceptions.exception_helper import ExceptionHelper
from python_utilities.json.json_helper import JSONHelper
from python_utilities.logging.logging_helper import LoggingHelper

# sourcenet imports
from sourcenet.models import Article
from sourcenet.models import Article_Data
from sourcenet.models import Article_Subject
from sourcenet.models import Person

# sourcenet_analysis imports
from sourcenet_analysis.models import Reliability_Names

#-------------------------------------------------------------------------------
# class definitions
#-------------------------------------------------------------------------------


class ReliabilityNamesBuilder( object ):
    
    
    #----------------------------------------------------------------------
    # constants-ish
    #----------------------------------------------------------------------    


    # Logger name
    LOGGER_NAME = "sourcenet_analysis.reliability.reliability_names_builder"

    # article info dictionary field names
    ARTICLE_ID = "article_id"
    ARTICLE_DATA_ID_LIST = "article_data_id_list"
    ARTICLE_CODER_ID_LIST = "article_coder_id_list"
    AUTHOR_INFO_DICT = "author_info_dict"
    SUBJECT_INFO_DICT = "subject_info_dict"
    
    # source and author info dicts will use same field names.
    PERSON_ID = "person_id"
    PERSON_NAME = "person_name"
    PERSON_LAST_NAME = "person_last_name"
    PERSON_FIRST_NAME = "person_first_name"
    PERSON_CODER_ID_TO_CODING_INFO_DICT = "person_coder_id_to_coding_info_dict"
    # PERSON_CODER_ID_LIST = "person_coder_id_list"
    
    # coder-specific person coding info map
    PERSON_CODING_INFO_CODER_ID = Reliability_Names.FIELD_NAME_SUFFIX_CODER_ID
    PERSON_CODING_INFO_PERSON_TYPE = Reliability_Names.FIELD_NAME_SUFFIX_PERSON_TYPE
    PERSON_CODING_INFO_PERSON_TYPE_INT = Reliability_Names.FIELD_NAME_SUFFIX_PERSON_TYPE_INT
    PERSON_CODING_INFO_ARTICLE_PERSON_ID = Reliability_Names.FIELD_NAME_SUFFIX_ARTICLE_PERSON_ID
    PERSON_CODING_INFO_FIRST_QUOTE_GRAF = Reliability_Names.FIELD_NAME_SUFFIX_FIRST_QUOTE_GRAF
    PERSON_CODING_INFO_FIRST_QUOTE_INDEX = Reliability_Names.FIELD_NAME_SUFFIX_FIRST_QUOTE_INDEX
    PERSON_CODING_INFO_ORGANIZATION_HASH = Reliability_Names.FIELD_NAME_SUFFIX_ORGANIZATION_HASH
    PERSON_CODING_INFO_NAME_LIST = [ PERSON_CODING_INFO_CODER_ID, PERSON_CODING_INFO_PERSON_TYPE, PERSON_CODING_INFO_PERSON_TYPE_INT, PERSON_CODING_INFO_ARTICLE_PERSON_ID, PERSON_CODING_INFO_FIRST_QUOTE_GRAF, PERSON_CODING_INFO_FIRST_QUOTE_INDEX, PERSON_CODING_INFO_ORGANIZATION_HASH ]
    
    # person types
    PERSON_TYPE_AUTHOR = "author"
    PERSON_TYPE_SUBJECT = "subject"
    PERSON_TYPE_SOURCE = "source"

    # Article_Subject subject_types
    SUBJECT_TYPE_MENTIONED = Article_Subject.SUBJECT_TYPE_MENTIONED
    SUBJECT_TYPE_QUOTED = Article_Subject.SUBJECT_TYPE_QUOTED

    # person or subject types to int ID map.
    PERSON_TYPE_TO_INT_MAP = {}
    PERSON_TYPE_TO_INT_MAP[ PERSON_TYPE_AUTHOR ] = 1
    PERSON_TYPE_TO_INT_MAP[ PERSON_TYPE_SUBJECT ] = 2
    PERSON_TYPE_TO_INT_MAP[ PERSON_TYPE_SOURCE ] = 3
    PERSON_TYPE_TO_INT_MAP[ SUBJECT_TYPE_MENTIONED ] = 2
    PERSON_TYPE_TO_INT_MAP[ SUBJECT_TYPE_QUOTED ] = 3
        
    # Organizations ERROR value
    ORG_HASH_ERROR_STRING = "ORG_HASH_ERROR"
    
    # information about table.
    TABLE_MAX_CODERS = 10

    
    #----------------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # declare instance variables
        self.article_id_to_info_map = {}
        self.coder_id_to_instance_map = {}        
        self.coder_id_to_index_map = {}
        
        # limit users included
        self.limit_to_user_ids = []
        self.exclude_user_ids = []
        
        # variable to hold desired automated coder type
        self.limit_to_automated_coder_type = ""
        self.automated_coder_type_include_list = []
        
        # exception helper
        self.exception_helper = ExceptionHelper()
        self.exception_helper.set_logger_name( self.LOGGER_NAME )
        
        # debug variables
        self.debug_output_json_file_path = ""
        
    #-- END method __init__() --#
    

    def add_coder_at_index( self, coder_id_IN, index_IN ):
        
        '''
        Accepts a coder ID and an index.  Updates all the stuff in this instance
            to make sure the coder is tied to the index passed in.
        '''
        
        # return reference
        status_OUT = ""
        
        # declare variables
        coder_id_to_index_dict = {}
        coder_id_to_instance_dict = {}
        limit_to_user_id_list = []
        coder_user_id = -1
        coder_index = -1
        coder_user = None
        
        # get maps from instance
        coder_id_to_index_dict = self.coder_id_to_index_map
        coder_id_to_instance_dict = self.coder_id_to_instance_map
        limit_to_user_id_list = self.limit_to_user_ids
        
        # init from input parameters.
        coder_user_id = coder_id_IN
        coder_index = index_IN
        
        # got ID?
        if ( ( coder_user_id is not None ) and ( int( coder_user_id ) > 0 ) ):
        
            # got index?
            if ( ( coder_index is not None ) and ( int( coder_index ) > 0 ) ):
            
                # yes.  Lookup the user.
                coder_user = User.objects.get( id = coder_user_id )
                
                # Set all the things up internally.
                coder_id_to_index_dict[ coder_user_id ] = coder_index
                coder_id_to_instance_dict[ coder_user_id ] = coder_user
                limit_to_user_id_list.append( coder_user_id )
                                
            else:
            
                # no index - broken.
                status_OUT = "No index - can't associate user with no index."
            
            #-- END check to see if index present. --#
        
        else:
        
            # no coder ID - broken.
            status_OUT = "No coder ID - can't associate user if no user."
        
        #-- END check to see if valid ID. --#

        return status_OUT        
        
    #-- END method add_coder_at_index() --#
    
        
    def build_reliability_names_data( self, tag_list_IN = None, label_IN = None ):
    
        '''
        Accepts tag list, label to apply to resulting Reliability_Names rows.
            Passes tag list to process_articles(), then passes the label to
            output_reliability_data().
        '''
        
        # return reference
        status_OUT = ""
    
        # got tag list?
        if ( ( tag_list_IN is not None ) and ( len( tag_list_IN ) > 0 ) ):
        
            # and got label?
            if ( ( label_IN is not None ) and ( label_IN != "" ) ):
            
                # got what we need.  Process articles.
                my_reliability_instance.process_articles( tag_list_IN )

                # output to database.
                my_reliability_instance.output_reliability_data( label_IN )
                
            else:
            
                # no label - error.
                status_OUT = "ERROR - must pass in a label."
            
            #-- END check to see if label --#
            
        else:
        
            # no tag list - error.
            status_OUT = "ERROR - must pass in a list of tags for filtering article data."

        #-- END check to see if tag list. --#
        
        return status_OUT
        
    #-- END method build_reliability_names_data() --#
    
        
    def filter_article_data( self, article_data_qs_IN ):
        
        '''
        Accepts Article_Data QuerySet.  Filters it based on any nested variables
            that relate to filtering.  Returns filtered QuerySet.
           
        Filters on:
            - self.limit_to_automated_coder_types - list of automated coder types we want included.
            - ).  Returns filtered QuerySet.
        '''
        
        # return reference
        qs_OUT = None
        
        # declare variables
        me = "filter_article_data"
        logging_message = ""
        my_logger = None
        automated_coder_type = None
        coder_type_list = None
        coder_id_include_list = None
        coder_id_exclude_list = None
        
        # init logger
        my_logger = LoggingHelper.get_a_logger( self.LOGGER_NAME )        
        
        # start by just returning what is passed in.
        qs_OUT = article_data_qs_IN
        
        # see if we have a single coder type.
        automated_coder_type = self.limit_to_automated_coder_type
        if ( ( automated_coder_type is not None ) and ( automated_coder_type != "" ) ):
        
            # got one.  Filter the QuerySet.
            coder_type_list = [ automated_coder_type, ]

            logging_message = "- limit to single coder type: " + str( automated_coder_type ) + "; coder_type_list = " + str( coder_type_list )
            # print( logging_message )
            my_logger.debug( "**** " + logging_message )            
        
        else:
        
            # no single value, check if there is a list.
            coder_type_list = self.automated_coder_type_include_list
        
            logging_message = "- limit automated coding to coder types in list: coder_type_list = " + str( coder_type_list )
            # print( logging_message )
            my_logger.debug( "**** " + logging_message )            
        
        #-- END check to see if automated coder type. --#
        
        # anything in automated coder type include list?
        if ( ( isinstance( coder_type_list, list ) == True ) and ( len( coder_type_list ) > 0 ) ):
        
            qs_OUT = Article_Data.filter_automated_by_coder_type( qs_OUT, coder_type_list )
        
        #-- END check to see if anything in coder_type_list.

        # got a list of coder IDs to limit to?
        coder_id_include_list = self.limit_to_user_ids
        if ( ( isinstance( coder_id_include_list, list ) == True ) and ( len( coder_id_include_list ) > 0 ) ):
        
            qs_OUT = qs_OUT.filter( coder__in = coder_id_include_list )
        
        #-- END check to see if anything in coder_type_list.

        # got a list of coder IDs to explicitly exclude?
        coder_id_exclude_list = self.exclude_user_ids
        if ( ( isinstance( coder_id_exclude_list, list ) == True ) and ( len( coder_id_exclude_list ) > 0 ) ):
        
            qs_OUT = qs_OUT.exclude( coder__in = coder_id_exclude_list )
        
        #-- END check to see if anything in coder_type_list.

        return qs_OUT
    
    #-- END method filter_article_data() --#


    def get_coder_for_index( self, index_IN ):
        
        '''
        Accepts a coder index.  Uses it to get ID of coder associated with that
           index, and returns instance of that User.  If none found, returns
           None.
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables
        coder_id_to_index_dict = {}
        coder_id_to_instance_dict = {}
        coder_user_id = -1
        coder_index = -1
        matching_user_id = -1
        
        # get maps from instance
        coder_id_to_index_dict = self.coder_id_to_index_map
        coder_id_to_instance_dict = self.coder_id_to_instance_map
        
        # first, use index to get coder ID.
        for coder_user_id, coder_index in six.iteritems( coder_id_to_index_dict ):
        
            # check to see if current index matches that passed in.
            if ( index_IN == coder_index ):
            
                # yes - store the ID.
                matching_user_id = coder_user_id
            
            #-- END check to see if indices match --#
            
        #-- END loop over ID-to-index map. --#
        
        #print( "++++ found ID: " + str( matching_user_id ) )
        
        # if we have an ID, use it to get User instance.
        if ( matching_user_id > 0 ):
        
            # we do.  Get instance from coder_id_to_instance_dict.
            instance_OUT = coder_id_to_instance_dict.get( matching_user_id, None )
            print( "++++ found User: " + str( instance_OUT ) )
        
        #-- END check to see if we have a User ID. --#
        
        return instance_OUT        
        
    #-- END method get_coder_for_index() --#
    
        
    def output_reliability_data( self, label_IN = "" ):
    
        '''
        Accepts article_info_dict_IN, dictionary that maps article IDs to the
           following:
           - article_id - ID of article.
           - article_data_id_list - list of IDs of Article_Data instances for the
              article.
           - article_coder_id_list - list of IDs of Coders who coded the article.
           - author_dict - dictionary that maps person IDs of authors to dictionary
              that contains details of author, including author ID, name, and 
              map of coder IDs who detected the author to their coding info for
              the author.
           - source_dict - dictionary that maps person IDs of sources to dictionary
              that contains details of source, including source ID, name, and
              map of coder IDs who detected the subject to their coding info for
              the subject.
              
        Loops over the items in the dictionary, processing each.  For each article,
           gets dictionaries of authors and sources and for each author and source,
           outputs a row to the reliability table containing coding information.
           
        Preconditions: expects that you already ran process_articles() with this
           instance.
        '''
    
        # declare variables.
        article_info_dict_IN = None
        article_info_count = -1
        article_info_counter = -1
        current_article_info_dict = {}
        my_article_id = -1
        my_article_info = {}
        my_article_data_id_list = []
        my_article_coder_id_list = []
        my_author_info_dict = {}
        my_subject_info_dict = {}
        my_article = None
        coder_id_to_index_dict = {}
        current_coder_index = -1
        coder_id_to_index_dict = {}
        my_person_id = -1
        my_person_info_dict = {}
        reliability_row = -1
        
        # get map of article IDs to attribution info.
        article_info_dict_IN = self.article_id_to_info_map
        
        # get map of coder IDs to their index number (1 up).
        coder_id_to_index_dict = self.coder_id_to_index_map
    
        # make sure we have something to output.
        if article_info_dict_IN is not None:
        
            # not None.  Initialize count variables.
            article_info_count = len( article_info_dict_IN )
            article_info_counter = 0
            
            # loop over info passed in.
            for my_article_id, my_article_info in six.iteritems( article_info_dict_IN ):
            
                # retrieve elements contained in article_info:
                my_article_data_id_list = my_article_info.get( self.ARTICLE_DATA_ID_LIST, [] )
                my_article_coder_id_list = my_article_info.get( self.ARTICLE_CODER_ID_LIST, [] )
                my_author_info_dict = my_article_info.get( self.AUTHOR_INFO_DICT, {} )
                my_subject_info_dict = my_article_info.get( self.SUBJECT_INFO_DICT, {} )
                
                # set up information needed for reliability row output.
                
                # get article for article ID.
                my_article = Article.objects.get( id = my_article_id )
                
                # for reliability table output, run through author and subject
                #    info, creating a row for each author and subject.
    
                # got author info?
                if ( ( my_author_info_dict is not None ) and ( len ( my_author_info_dict ) > 0 ) ):
                
                    # loop over the info in the dictionary, calling function to
                    #    output a given person's row to the reliability table
                    #    for each.
                    for my_person_id, my_person_info_dict in six.iteritems( my_author_info_dict ):
                    
                        # call function to output reliability table row.
                        reliability_row = self.output_reliability_name_row( my_article, my_person_info_dict, self.PERSON_TYPE_AUTHOR, label_IN = label_IN )
                        print ( "- author: " + str( reliability_row ) )
                    
                    #-- END loop over author info ---#
                
                #-- END check to see if we have author info. --#
                
                # got subject info?
                if ( ( my_subject_info_dict is not None ) and ( len ( my_subject_info_dict ) > 0 ) ):
                
                    # loop over the info in the dictionary, calling function to
                    #    output a given person's row to the reliability table
                    #    for each.
                    for my_person_id, my_person_info_dict in six.iteritems( my_subject_info_dict ):
                    
                        # call function to output reliability table row.
                        reliability_row = self.output_reliability_name_row( my_article, my_person_info_dict, self.PERSON_TYPE_SUBJECT, label_IN = label_IN )
                        print ( "- source: " + str( reliability_row ) )
                    
                    #-- END loop over author info ---#
    
                #-- END check to see if we have author info. --#            
            
            #-- END loop over article_info_dict_IN --#
            
        #-- END check to see if we got something passed in. --#
        
    #-- END method output_reliability_data --##
    
    
    def output_reliability_name_row( self, article_IN, person_info_dict_IN, article_person_type_IN, label_IN = "" ):
        
        '''
        Accepts:
        - article_IN - article this person was detected within.
        - person_info_dict_IN, dictionary that maps person IDs to the
            following:
            - person_id - ID of person found in article.
            - person_name - String name of that person.
            - person_coder_id_to_coding_info_dict - dictionary that maps IDs of
                coders who detected and recorded the presence of that person to
                details of their coding.  For now, just has coder ID, person
                type, and Article_Person record ID.  Could have more information
                in the future.
        - article_person_type_IN, the type of the Article_Person children we are
            processing ("author" or "subject").
        - label_IN - label to assign to this set of data in the database.
         
        Creates an instance of Reliability_Names, stores values from
            the dictionary in the appropriate columns, then saves it.
           
        Returns the row model instance, or None if error.
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables
        me = "output_reliability_name_row"
        my_logger = None
        logging_message = ""
        coder_id_to_index_map_IN = None
        reliability_instance = None
        my_person_id = -1
        my_person = None
        my_person_name = ""
        my_person_first_name = ""
        my_person_last_name = ""
        my_coder_person_info_dict = None
        coder_count = -1
        current_coder_id = -1
        current_person_coding_info = None
        current_coder_index = -1
        current_coder_user = None
        current_coding_info_name = None
        current_coding_info_value = None
        index_used_list = []
        current_number = -1
        current_index = -1
        
        # declare variables - getting appropriate Article_Data for automated
        article_data_qs = None
        coder_article_data_qs = None
        coder_article_data = None
        coder_article_data_id = -1
        
        # init logger
        my_logger = LoggingHelper.get_a_logger( self.LOGGER_NAME )        
        
        # make sure we have everything we need.
        coder_id_to_index_map_IN = self.coder_id_to_index_map

        # article
        if ( article_IN is not None ):
    
            # retrieve the Article_Data QuerySet.    
            article_data_qs = article_IN.article_data_set.all()
        
            # person_info
            if ( person_info_dict_IN is not None ):
            
                # map of coder IDs to indexes
                if ( coder_id_to_index_map_IN is not None ):
                
                    # person type.
                    if ( ( article_person_type_IN is not None ) and ( article_person_type_IN != "" ) ):
                    
                        # got everything.  make reliability row.
                        reliability_instance = Reliability_Names()
                        
                        # got a label?
                        if ( ( label_IN is not None ) and ( label_IN != "" ) ):
                        
                            # yes, there is a label.  Add it to row.
                            reliability_instance.label = label_IN
                        
                        #-- END check to see if label --#
                        
                        # get information from info dictionary
                        my_person_id = person_info_dict_IN.get( self.PERSON_ID, -1 )
                        my_person = Person.objects.get( id = my_person_id )
                        my_person_name = person_info_dict_IN.get( self.PERSON_NAME, None )
                        my_person_first_name = person_info_dict_IN.get( self.PERSON_FIRST_NAME, None )
                        my_person_last_name = person_info_dict_IN.get( self.PERSON_LAST_NAME, None )
                        my_coder_person_info_dict = person_info_dict_IN.get( self.PERSON_CODER_ID_TO_CODING_INFO_DICT, {} )
                        
                        # place info inside
                        reliability_instance.article = article_IN
                        reliability_instance.person = my_person
                        reliability_instance.person_name = my_person_name
                        reliability_instance.person_first_name = my_person_first_name
                        reliability_instance.person_last_name = my_person_last_name
                        reliability_instance.person_type = article_person_type_IN
                        
                        # check to see if more than TABLE_MAX_CODERS.
                        coder_count = len( my_coder_person_info_dict )
                        if ( coder_count > self.TABLE_MAX_CODERS ):
                        
                            # bad news - print error.
                            print ( "====> In " + me + ": ERROR - more coders ( " + str( coder_count ) + " ) than table allows ( " + str( self.TABLE_MAX_CODERS ) + " ).\"" )
                            
                        #-- END check to see if more coders than slots in table --#
                        
                        # loop over coders.
                        for current_coder_id, current_person_coding_info in six.iteritems( my_coder_person_info_dict ):
                        
                            # look up index.
                            current_coder_index = coder_id_to_index_map_IN.get( current_coder_id, -1 )
                            
                            # get User instance
                            current_coder_user = User.objects.get( id = current_coder_id )
                            
                            # retrieve coder's Article_Data.
                            coder_article_data = None
                            coder_article_data_id = -1
                            coder_article_data_qs = article_data_qs.filter( coder = current_coder_user )
                            
                            # ! put before and after logging here.
                            
                            logging_message = "- in " + me + "(): before filtering, coder_article_data_qs.count() = " + str( coder_article_data_qs.count() )
                            #print( logging_message )
                            my_logger.debug( "**** " + logging_message )            
                            
                            # ! if automated, filter on coder_type
                            coder_article_data_qs = self.filter_article_data( coder_article_data_qs )
                            
                            logging_message = "- in " + me + "(): after filtering, coder_article_data_qs.count() = " + str( coder_article_data_qs.count() )
                            #print( logging_message )
                            my_logger.debug( "**** " + logging_message )            

                            # how many?
                            if ( coder_article_data_qs.count() == 1 ):
                            
                                # got one! store information.
                                coder_article_data = coder_article_data_qs.get()
                                coder_article_data_id = coder_article_data.id
                            
                            #-- END check to see if single matching Article_Data --#    
                                
                            # use index to decide in which columns to place
                            #    coder-specific information.
                            if ( current_coder_index != -1 ):
                            
                                # add index to used list if not already there
                                if current_coder_index not in index_used_list:

                                    index_used_list.append( current_coder_index )
                                    
                                else:
                                
                                    # ! TODO - add logging.
                                    # already there?  Error.
                                    logging_message = "====> In " + me + ": ERROR - index already used - multiple records for coder ID \"" + str( current_coder_id ) + "\""
                                    print( logging_message )
                                    my_logger.debug( "**** " + logging_message )            

                                #-- END check to see if index is in our "used" list --#
                            
                                # place info in "coder<index>" fields.
                                
                                # coder# - reference to User who coded.
                                field_name = "coder" + str( current_coder_index )
                                setattr( reliability_instance, field_name, current_coder_user )
                                
                                # coder#_detected - 1, since coder detected this person.
                                field_name = "coder" + str( current_coder_index ) + "_detected"
                                setattr( reliability_instance, field_name, 1 )
    
                                # coder#_person_id - id of person (will be
                                #    subsequently used to smoosh rows together for
                                #    same name, different person IDs).
                                field_name = "coder" + str( current_coder_index ) + "_person_id"
                                setattr( reliability_instance, field_name, my_person_id )
                                
                                # ! loop over coding info
                                
                                # set fields from current_person_coding_info.
                                #     Each name in dictionary corresponds to
                                #     column in database table.
                                for current_coding_info_name, current_coding_info_value in six.iteritems( current_person_coding_info ):
                                
                                    # set field name using name.
                                    field_name = "coder" + str( current_coder_index ) + "_" + current_coding_info_name
                                    
                                    # use that field name to set value.
                                    setattr( reliability_instance, field_name, current_coding_info_value )
                                    
                                #-- END loop over coding info. --#

                                # coder#_article_data_id - id of coder's
                                #    Article_Data row.
                                # Got an ID?
                                if ( coder_article_data_id > 0 ):
                                
                                    # yes.  store it.
                                    field_name = "coder" + str( current_coder_index ) + "_article_data_id"
                                    setattr( reliability_instance, field_name, coder_article_data_id )
                                
                                #-- END check to see if Article_Data ID --#
                            
                            else:
                            
                                print ( "====> In " + me + ": ERROR - no index found for coder ID \"" + str( current_coder_id ) + "\"" )
    
                            #-- END check to make sure coder index isn't -1 --#
                        
                        #-- END loop over coder IDs. --#
                        
                        print( "----> In " + me + ": len( index_used_list ) = " + str( len( index_used_list ) ) )
                        
                        # check to make sure that all indexes were used.
                        if ( len( index_used_list ) < self.TABLE_MAX_CODERS ):
                        
                            # not all used.  put zeroes in fields for indices
                            #    not in the list.
                            for current_number in range( self.TABLE_MAX_CODERS ):
                            
                                # increment value by 1.
                                current_index = current_number + 1
                                
                                # is it in the list?
                                if ( current_index not in index_used_list ):
                                
                                    # no - add values.
                                    
                                    # If you are going to be calculating
                                    #     reliability on a numeric column, you
                                    #     need to set it to 0 here for coders
                                    #     who did not detect the current person,
                                    #     else you'll have NaN problems in R.
                                    # If you don't set it here, column will get
                                    #     default value, usually NULL in SQL.

                                    # coder# - reference to User who coded.
                                    current_coder_user = self.get_coder_for_index( current_index )
                                    field_name = "coder" + str( current_index )
                                    setattr( reliability_instance, field_name, current_coder_user )
                                    
                                    # coder#_detected - 0, since coder did not
                                    #    detect this person.
                                    field_name = "coder" + str( current_index ) + "_detected"
                                    setattr( reliability_instance, field_name, 0 )
        
                                    # coder#_person_id - id of person (0, since
                                    #    coder didn't detect this person).
                                    field_name = "coder" + str( current_index ) + "_person_id"
                                    setattr( reliability_instance, field_name, 0 )
                                                                    
                                    # coder#_person_type_int - person type of 
                                    #    person (0, since coder didn't detect
                                    #    this person).
                                    field_name = "coder" + str( current_index ) + "_person_type_int"
                                    setattr( reliability_instance, field_name, 0 )
                                                                    
                                
                            #-- END loop over numbers 1 through TABLE_MAX_CODERS --#
                            
                        #-- END check to see if all indices used. --#
                        
                        # save
                        reliability_instance.save()
                        
                        # return
                        instance_OUT = reliability_instance
        
                    #-- END check to see if we have person type. --#
    
                #-- END check to see if we have map of coder IDs to indexes. --#
    
            #-- END check to see if we have person info. --#
    
        #-- END check to see if we have an article. --#
        
        return instance_OUT
        
    #-- END method output_reliability_name_row() --#


    def process_articles( self, tag_list_IN = [], limit_to_sources_IN = False ):

        '''
        Grabs articles with a tag in tag_list_IN.  For each, loops through their
           Article_Data to build a dictionary that maps article ID to article
           info. that includes:
           - article_id - ID of article.
           - article_data_id_list - list of IDs of Article_Data instances for the
              article.
           - article_coder_id_list - list of IDs of Coders who coded the article.
           - author_dict - dictionary that maps person IDs of authors to dictionary
              that contains details of author, including author ID, name, and list of
              coders who found the author.
           - source_dict - dictionary that maps person IDs of sources to dictionary
              that contains details of source, including source ID, name, and list of
              coders who found the source.
        '''

        # declare variables - retrieving reliability sample.
        me = "process_articles"
        my_logger = None
        logging_message = ""
        article_qs = None
        current_article = None
        article_data_qs = None
        current_query = None
        article_data_count = -1
        
        # declare variables - compiling information for articles.
        article_id = -1
        article_to_info_dict = None
        article_info_dict = None
        coder_id_to_instance_dict = None
        coder_id_to_index_dict = None
        coder_counter = -1
        current_article_data = None
        article_data_id_list = None
        article_data_author_qs = None
        article_data_subject_qs = None
        article_coder_id_list = None
        article_data_id = -1
        article_data_coder = None
        article_data_coder_id = None
        person_type = ""
        author_info_dict = None
        subject_info_dict = None
        
        # declare variables - debug output.
        debug_file_output_path = ""
        json_string = ""
        json_file_handle = None

        # init logger
        my_logger = LoggingHelper.get_a_logger( self.LOGGER_NAME )
        
        #-------------------------------------------------------------------------------
        # process articles to build data
        #-------------------------------------------------------------------------------
        
        # got a tag list?
        if ( ( tag_list_IN is not None ) and ( len( tag_list_IN ) > 0 ) ):

            # get articles with tags in list passed in.
            article_qs = Article.objects.filter( tags__name__in = tag_list_IN )
            
        #-- END check to see if tag list --#
            
        article_qs = article_qs.order_by( "id" )
        
        # build a dictionary that maps article ID to assorted details about the coding
        #    of each article.
        article_to_info_dict = self.article_id_to_info_map
        
        # For reference, also build up a dictionary of coder IDs that reference
        #    coder instances, so we know how many coders, and coder IDs to
        #    index, from 1 up, so we can keep them straight when outputting
        #    data.
        coder_id_to_instance_dict = self.coder_id_to_instance_map
        coder_id_to_index_dict = self.coder_id_to_index_map
        coder_counter = 0
        
        # loop over the articles.
        for current_article in article_qs:
        
            # initialize variables
            article_info_dict = {}
            article_data_id_list = []
            article_coder_id_list = []
            author_info_dict = {}
            subject_info_dict = {}
        
            # get article_id
            article_id = current_article.id
        
            # get article data for this article
            article_data_qs = current_article.article_data_set.all()
            
            # ! filter on automated coder_type, IDs of coders to include or
            #     exclude, if filters are specified.
            article_data_qs = self.filter_article_data( article_data_qs )
            
            # how many Article_Data?
            article_data_count = len( article_data_qs )
        
            # output summary row.
            logging_message = "- Article ID: " + str( current_article.id ) + "; Article_Data count: " + str( article_data_count )
            print( logging_message )
            my_logger.debug( "**** " + logging_message )
            
            # for each article, build a dictionary that maps article ID to article info.
            #    that includes:
            # - article_id - ID of article.
            # - article_data_id_list - list of IDs of Article_Data instances for the
            #    article.
            # - article_coder_id_list - list of IDs of Coders who coded the article.
            # - author_dict - dictionary that maps person IDs of authors to dictionary
            #    that contains details of author, including author ID, name, and list of
            #    coders who found the author.
            # - source_dict - dictionary that maps person IDs of sources to dictionary
            #    that contains details of source, including source ID, name, and list of
            #    coders who found the source.
            
            # check to see if article already has an info dictionary (it better not...).
            if article_id in article_to_info_dict:
            
                # retrieve info dictionary
                article_info_dict = article_to_info_dict.get( article_id, {} )
                
            else:
            
                # make new info dictionary and add reference to it to master dictionary.
                article_info_dict = {}
                article_to_info_dict[ article_id ] = article_info_dict
                
            #-- END check to see if article already has an information dictionary. --#
            
            # compile information.
            
            # loop over related Article_Data instances.
            for current_article_data in article_data_qs:
            
                # output summary row.
                logging_message = "---- - Article Data Info: " + str( current_article_data )
                print( logging_message )
                my_logger.debug( "******** " + logging_message )
    
                # get coder and coder's User ID.
                article_data_coder = current_article_data.coder
                article_data_coder_id = article_data_coder.id
                
                # make sure that:
                # - there either isn't a list of users to include, OR if there
                #     is a list of users to include, the coder is in the list.
                # - AND there either isn't a list of users to exclude, OR if
                #     there is a list of users to exclude, the coder is not in
                #     the list.
                if ( ( ( len( self.limit_to_user_ids ) == 0 ) or ( article_data_coder_id in self.limit_to_user_ids ) )
                    and ( ( len( self.exclude_user_ids ) == 0 ) or ( article_data_coder_id not in self.exclude_user_ids ) ) ):
                
                    # If not already there, add to list of IDs of coders for this article.
                    if article_data_coder_id not in article_coder_id_list:
            
                        # not there yet, add it.
                        article_coder_id_list.append( article_data_coder_id )
                        
                    #-- END check to see if ID is in coder ID list --#
                
                    # If not already there, add to master coder dictionary, also.
                    if article_data_coder_id not in coder_id_to_instance_dict:
            
                        # not there yet.  Increment coder counter.
                        coder_counter += 1
                        
                        # add coder to instance cache.
                        coder_id_to_instance_dict[ article_data_coder_id ] = article_data_coder
                        
                        # and add to index map.
                        coder_id_to_index_dict[ article_data_coder_id ] = coder_counter
                        
                    #-- END check to see if ID is in master coder dictionary --#
                                
                    # add Article_Data ID to list.
                    article_data_id = current_article_data.id
                    article_data_id_list.append( article_data_id )
                    
                    # get lists of authors and subjects.
                    article_data_author_qs = current_article_data.article_author_set.all()
    
                    # all subjects, or just sources?
                    if ( limit_to_sources_IN == True ):
    
                        # just sources.
                        article_data_subject_qs = current_article_data.get_quoted_article_sources_qs()
                        
                    else:
                    
                        # all subjects (the default).
                        article_data_subject_qs = current_article_data.article_subject_set.all()
                        
                    #-- END check to see if all subjects or just sources. --#
                    
                    # call process_person_qs for authors.
                    person_type = self.PERSON_TYPE_AUTHOR
                    author_info_dict = self.process_person_qs( article_data_coder, article_data_author_qs, author_info_dict, person_type )
                            
                    # and call process_person_qs for subjects.
                    person_type = self.PERSON_TYPE_SUBJECT
                    subject_info_dict = self.process_person_qs( article_data_coder, article_data_subject_qs, subject_info_dict, person_type )
                    
                else:
                
                    # not processing coding by this user.  Move on.
                    pass
                    
                #-- END check to see if we are including current user's coding. --#
                        
            #-- END loop over related Article_Data
            
            # update article info dictionary
            article_info_dict[ self.ARTICLE_ID ] = article_id
            article_info_dict[ self.ARTICLE_DATA_ID_LIST ] = article_data_id_list
            article_info_dict[ self.ARTICLE_CODER_ID_LIST ] = article_coder_id_list
            article_info_dict[ self.AUTHOR_INFO_DICT ] = author_info_dict
            article_info_dict[ self.SUBJECT_INFO_DICT ] = subject_info_dict    
        
            # shouldn't need to do anything more - reference to this dictionary is
            #    already in the master map of article IDs to article info.
        
        #-- END loop over articles. --#
        
        # ! output debug JSON to a file?
        debug_file_output_path = self.debug_output_json_file_path
        if ( ( debug_file_output_path is not None ) and ( debug_file_output_path != "" ) ):
        
            # user wants us to try to output JSON.
            json_string = JSONHelper.pretty_print_json( self.article_id_to_info_map )

            # open file and write json_string to it.
            with open( debug_file_output_path, "w" ) as json_file_handle:
            
                # write out the json string.
                json_file_handle.write( json_string )
            
            #-- END with json_file_handle --#
        
        #-- END check to see if we output debug JSON. --#

    #-- END method process_articles() --#


    def process_person_qs( self, coder_IN, article_person_qs_IN, person_info_dict_IN, article_person_type_IN ):
        
        '''
        Accepts User instance of user who coded the Article, Article_Person
            QuerySet (either Article_Author or Article_Subject) and a dictionary
            to be used to build up a map of IDs to information on people found
            in a given article. Loops over entries and builds up this dictionary
            that maps IDs of persons identified in the text to details on the
            person (including the Person's ID, string name, and a map of coder
            IDs to a dictionary for each coder who detected that person with
            their coding info, at this point their ID and the type they assigned
            to the person).  Returns the updated person_info_dict dictionary.
        '''
        
        # return reference
        person_info_dict_OUT = {}
        
        # declare variables
        me = "process_person_qs"
        my_logger = None
        current_article_person = None
        coder_id = -1
        person_instance = None
        person_id = -1
        person_name = ""
        person_parsed_name = None
        person_info = None
        person_coding_info_dict = None
        person_coding_info = None
        current_person_type = None
        current_person_type_int = None
        current_organization = ""
        encoded_organization = ""
        org_hash_object = None
        org_hash = ""

        # declare variables - subject-specific processing.
        is_subject = False
        subject_quote_qs = None
        subject_quote_count = -1
        subject_first_quote = None
        first_quote_graf = -1
        first_quote_index = -1
        
        # init logger
        my_logger = LoggingHelper.get_a_logger( self.LOGGER_NAME )
        
        # make sure we have a coder
        if ( coder_IN is not None ):
        
            # make sure we have a queryset.
            if ( article_person_qs_IN is not None ):
            
                # make sure we have a person type passed in.
                if ( ( article_person_type_IN is not None ) and ( article_person_type_IN != "" ) ):
            
                    # log the current person.
                    my_logger.debug( "--------> In " + me + ": current person type = " + str( article_person_type_IN ) )
                    
                    # got a dictionary passed in?
                    if ( person_info_dict_IN is not None ):
                    
                        person_info_dict_OUT = person_info_dict_IN
                    
                    #-- END check to see if we have a dictionary passed in. --#
            
                    # compile information on authors.
                    for current_article_person in article_person_qs_IN:
                    
                        # log the current person.
                        my_logger.debug( "====> In " + me + ": current person = " + str( current_article_person ) )
                        
                        # get coder ID.
                        coder_id = coder_IN.id
                        
                        # get current person type, different way based on person
                        #     type passed in.
                        # Article_Author QuerySet?
                        if ( article_person_type_IN == self.PERSON_TYPE_AUTHOR ):
                        
                            # only one type of author, so use the type passed in.
                            current_person_type = article_person_type_IN
                            is_subject = False
                        
                        # Article_Subject QuerySet?
                        elif ( ( article_person_type_IN == self.PERSON_TYPE_SUBJECT )
                            or ( article_person_type_IN == self.PERSON_TYPE_SOURCE ) ):
                        
                            # this is an Article_Subject, so get subject_type.
                            current_person_type = current_article_person.subject_type
                            is_subject = True
                            
                            # might have None.  If so, default to mentioned.
                            if ( current_person_type is None ):
                            
                                # it is None.  Sigh.  Default to mentioned.
                                current_person_type = self.SUBJECT_TYPE_MENTIONED
                            
                            #-- END check to see if person type is None --#
                        
                        else:
                        
                            # unknown Article_Person type.  set to empty string.
                            current_person_type = ""
                            is_subject = False
                        
                        #-- END check to see how we get person type. --#
                        
                        # log the current type.
                        my_logger.debug( "In " + me + ": current person type = " + str( current_person_type ) + " - to int map = " + str( self.PERSON_TYPE_TO_INT_MAP ) )
                        
                        # also get integer value
                        current_person_type_int = self.PERSON_TYPE_TO_INT_MAP.get( current_person_type, -1 )

                        # log the current type.
                        my_logger.debug( "In " + me + ": current person type as int = " + str( current_person_type_int ) )
                                                
                        # get person instance.
                        person_instance = current_article_person.person
                    
                        # got one?  Anonymous sources won't have one.  If we find a
                        #    record with no associated person, move on.
                        if ( person_instance is not None ):
                    
                            # get person ID and name values.
                            person_id = person_instance.id
                            person_name = person_instance.get_name_string()
                            person_parsed_name = person_instance.to_HumanName()
                            
                            # create coding info. for this coder.
                            person_coding_info = {}
                            
                            # ! Place data in person_coding_info
                            
                            # coder ID
                            person_coding_info[ self.PERSON_CODING_INFO_CODER_ID ] = coder_id
                            
                            # person type
                            person_coding_info[ self.PERSON_CODING_INFO_PERSON_TYPE ]  = current_person_type
                            person_coding_info[ self.PERSON_CODING_INFO_PERSON_TYPE_INT ]  = current_person_type_int
                            
                            # Article_Person child record ID.
                            person_coding_info[ self.PERSON_CODING_INFO_ARTICLE_PERSON_ID ] = current_article_person.id
                            
                            # if subject, tack on information on first quote
                            if ( is_subject == True ):
                            
                                # FIELD_NAME_SUFFIX_FIRST_QUOTE_GRAF = "first_quote_graf"
                                # FIELD_NAME_SUFFIX_FIRST_QUOTE_INDEX = "first_quote_index"
                                
                                # check to see if person has any quotes.
                                subject_quote_qs = current_article_person.article_subject_quotation_set.all()
                                subject_quote_count = subject_quote_qs.count()
                                if ( subject_quote_count > 0 ):
                                
                                    # we do.  Order by paragraph number, then
                                    #    index.
                                    subject_quote_qs = subject_quote_qs.order_by( "paragraph_number", "value_index" )
                                    
                                    # get the first record in the list.
                                    subject_quote_qs = subject_quote_qs[ : 1 ]
                                    subject_first_quote = subject_quote_qs.get()
                                    
                                    # retrieve and store the paragraph and index
                                    #    values
                                    first_quote_graf = subject_first_quote.paragraph_number
                                    first_quote_index = subject_first_quote.value_index
                                    
                                    # and store them.
                                    person_coding_info[ self.PERSON_CODING_INFO_FIRST_QUOTE_GRAF ] = first_quote_graf
                                    person_coding_info[ self.PERSON_CODING_INFO_FIRST_QUOTE_INDEX ] = first_quote_index
                                
                                #-- END check to see if we have quotes --#
                                
                            #-- END check to see if is subject. --#

                            # FIELD_NAME_SUFFIX_ORGANIZATION_HASH = "organization_hash"
                            current_organization = current_article_person.organization_string
                            
                            # see if there is an organization
                            if ( ( current_organization is not None ) and ( current_organization != "" ) ):
                            
                                # to start, wrap in try in case there are encoding
                                #    problems.
                                try:
                                
                                    # encode the string to "utf-8"
                                    encoded_organization = current_organization.encode( "utf-8" )
                                    
                                    # convert to sha256
                                    org_hash_object = hashlib.sha256( encoded_organization )
                                    org_hash = org_hash_object.hexdigest()
                                    
                                except Exception as e:
                                
                                    # exception
                                    self.exception_helper.process_exception( exception_IN = e, message_IN = "Exception caught converting organization_string to sha256 hash." )
                                
                                    # On error, store self.ORG_HASH_ERROR_STRING
                                    org_hash = self.ORG_HASH_ERROR_STRING
    
                                #-- END try/except --#
                                
                            else:
                            
                                # no organization, set to None.
                                org_hash = None
                                
                            #-- END check to see if any organization value to hash --#
                                
                            # store org_hash in person_coding_info
                            person_coding_info[ self.PERSON_CODING_INFO_ORGANIZATION_HASH ] = org_hash
    
                            # look for person in person info dictionary.
                            if person_id in person_info_dict_OUT:
                            
                                # person already encountered.  Add coding info
                                #    to the coding info list.
                                person_info = person_info_dict_OUT.get( person_id )
                                
                                # get person_coding_info_list.
                                person_coding_info_dict = person_info.get( self.PERSON_CODER_ID_TO_CODING_INFO_DICT )
                                
                                # append person_coding_info
                                person_coding_info_dict[ coder_id ] = person_coding_info
                                
                            else:
                            
                                # person not in the dictionary yet.  Create new dictionary.
                                person_info = {}
                                
                                # add information.
                                person_info[ self.PERSON_ID ] = person_id
                                person_info[ self.PERSON_NAME ] = person_name
                                person_info[ self.PERSON_FIRST_NAME ] = person_parsed_name.first
                                person_info[ self.PERSON_LAST_NAME ] = person_parsed_name.last
                                
                                # add person coding info. for this coder.
                                person_coding_info_dict = {}
                                person_coding_info_dict[ coder_id ] = person_coding_info
                                person_info[ self.PERSON_CODER_ID_TO_CODING_INFO_DICT ] = person_coding_info_dict
                                
                                # add info to return dictionary.
                                person_info_dict_OUT[ person_id ] = person_info
                                
                            #-- END check to see if person is already in the dictionary. --#
                            
                        else:
                        
                            # no person - output a message.
                            print( "In " + me + ": no person found for record: " + str( current_article_person ) )
                            
                        #-- END check to make sure that person is present. --#
            
                    #-- END loop over persons. --#
                    
                #-- END check to see if we have person type. --#
                
            #-- END check to see if QuerySet passed in. --#  
        
        #-- END check to see if Coder present --#
        
        return person_info_dict_OUT
        
    #-- END method process_person_qs() --#


#-- END class ReliabilityNamesBuilder --#
