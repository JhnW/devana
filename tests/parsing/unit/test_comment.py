import unittest
import os
from devana.syntax_abstraction.organizers.sourcefile import SourceFile
from devana.syntax_abstraction.comment import Comment, CommentsFactory, CommentMarker
from devana.configuration import Configuration, ParsingConfiguration, LanguageStandard


class TestComment(unittest.TestCase):

    def setUp(self):
        self.source_file = SourceFile(os.path.dirname(__file__) + r"/source_files/comments/comment_basic.hpp")
        self.comments_factory = CommentsFactory(self.source_file)

    def test_crate_all_comments(self):
        self.assertEqual(len(self.comments_factory.comments), 10)

    def test_comments_markers(self):
        self.assertEqual(self.comments_factory.comments[0].marker, CommentMarker.ONE_LINE)
        self.assertEqual(self.comments_factory.comments[1].marker, CommentMarker.MULTI_LINE)
        self.assertEqual(self.comments_factory.comments[2].marker, CommentMarker.ONE_LINE)
        self.assertEqual(self.comments_factory.comments[3].marker, CommentMarker.ONE_LINE)
        self.assertEqual(self.comments_factory.comments[4].marker, CommentMarker.MULTI_LINE)
        self.assertEqual(self.comments_factory.comments[5].marker, CommentMarker.MULTI_LINE)
        self.assertEqual(self.comments_factory.comments[6].marker, CommentMarker.MULTI_LINE)
        self.assertEqual(self.comments_factory.comments[7].marker, CommentMarker.MULTI_LINE)
        self.assertEqual(self.comments_factory.comments[8].marker, CommentMarker.ONE_LINE)
        self.assertEqual(self.comments_factory.comments[9].marker, CommentMarker.MULTI_LINE)

    def test_comments_locations_begin(self):
        self.assertEqual(self.comments_factory.comments[0].begin.row, 1)
        self.assertEqual(self.comments_factory.comments[1].begin.row, 2)
        self.assertEqual(self.comments_factory.comments[2].begin.row, 4)
        self.assertEqual(self.comments_factory.comments[3].begin.row, 5)
        self.assertEqual(self.comments_factory.comments[4].begin.row, 7)
        self.assertEqual(self.comments_factory.comments[5].begin.row, 13)
        self.assertEqual(self.comments_factory.comments[6].begin.row, 18)
        self.assertEqual(self.comments_factory.comments[7].begin.row, 23)
        self.assertEqual(self.comments_factory.comments[8].begin.row, 30)
        self.assertEqual(self.comments_factory.comments[9].begin.row, 31)

        self.assertEqual(self.comments_factory.comments[0].begin.col, 1)
        self.assertEqual(self.comments_factory.comments[1].begin.col, 1)
        self.assertEqual(self.comments_factory.comments[2].begin.col, 1)
        self.assertEqual(self.comments_factory.comments[3].begin.col, 1)
        self.assertEqual(self.comments_factory.comments[4].begin.col, 1)
        self.assertEqual(self.comments_factory.comments[5].begin.col, 1)
        self.assertEqual(self.comments_factory.comments[6].begin.col, 5)
        self.assertEqual(self.comments_factory.comments[7].begin.col, 1)
        self.assertEqual(self.comments_factory.comments[8].begin.col, 5)
        self.assertEqual(self.comments_factory.comments[9].begin.col, 5)

    def test_comments_locations_end(self):
        self.assertEqual(self.comments_factory.comments[0].end.row, 1)
        self.assertEqual(self.comments_factory.comments[1].end.row, 2)
        self.assertEqual(self.comments_factory.comments[2].end.row, 4)
        self.assertEqual(self.comments_factory.comments[3].end.row, 5)
        self.assertEqual(self.comments_factory.comments[4].end.row, 11)
        self.assertEqual(self.comments_factory.comments[5].end.row, 16)
        self.assertEqual(self.comments_factory.comments[6].end.row, 21)
        self.assertEqual(self.comments_factory.comments[7].end.row, 28)
        self.assertEqual(self.comments_factory.comments[8].end.row, 30)
        self.assertEqual(self.comments_factory.comments[9].end.row, 31)

        self.assertEqual(self.comments_factory.comments[0].end.col, 8)
        self.assertEqual(self.comments_factory.comments[1].end.col, 10)
        self.assertEqual(self.comments_factory.comments[2].end.col, 10)
        self.assertEqual(self.comments_factory.comments[3].end.col, 10)
        self.assertEqual(self.comments_factory.comments[4].end.col, 2)
        self.assertEqual(self.comments_factory.comments[5].end.col, 2)
        self.assertEqual(self.comments_factory.comments[6].end.col, 6)
        self.assertEqual(self.comments_factory.comments[7].end.col, 2)
        self.assertEqual(self.comments_factory.comments[8].end.col, 12)
        self.assertEqual(self.comments_factory.comments[9].end.col, 14)

    def test_comments_text(self):
        comment: Comment = self.comments_factory.comments[0]
        self.assertEqual(len(comment.text), 1)
        self.assertEqual(comment.text[0], "test 1")

        comment: Comment = self.comments_factory.comments[1]
        self.assertEqual(len(comment.text), 1)
        self.assertEqual(comment.text[0], "test 2")

        comment: Comment = self.comments_factory.comments[2]
        self.assertEqual(len(comment.text), 1)
        self.assertEqual(comment.text[0], "test 3.1")

        comment: Comment = self.comments_factory.comments[3]
        self.assertEqual(len(comment.text), 1)
        self.assertEqual(comment.text[0], "test 3.2")

        comment: Comment = self.comments_factory.comments[4]
        self.assertEqual(len(comment.text), 3)
        self.assertEqual(comment.text[0], "test 4.1")
        self.assertEqual(comment.text[1], "test 4.2")
        self.assertEqual(comment.text[2], "test 4.3")

        comment: Comment = self.comments_factory.comments[5]
        self.assertEqual(len(comment.text), 3)
        self.assertEqual(comment.text[0], "test 5.1")
        self.assertEqual(comment.text[1], "test 5.2")
        self.assertEqual(comment.text[2], "test 5.3")

        comment: Comment = self.comments_factory.comments[6]
        self.assertEqual(len(comment.text), 2)
        self.assertEqual(comment.text[0], "test 6.1")
        self.assertEqual(comment.text[1], "test 6.2")

        comment: Comment = self.comments_factory.comments[7]
        self.assertEqual(len(comment.text), 4)
        self.assertEqual(comment.text[0], "test 7.1")
        self.assertEqual(comment.text[1], "test 7.2")
        self.assertEqual(comment.text[2], "test 7.3")
        self.assertEqual(comment.text[3], "//test 7.4")

        comment: Comment = self.comments_factory.comments[8]
        self.assertEqual(len(comment.text), 1)
        self.assertEqual(comment.text[0], "test 8")

        comment: Comment = self.comments_factory.comments[9]
        self.assertEqual(len(comment.text), 1)
        self.assertEqual(comment.text[0], "test 9")


class TestCommentFactoryAssigned(unittest.TestCase):

    def setUp(self):
        self.source_file = SourceFile(
            os.path.dirname(__file__) + r"/source_files/comments/comment_elements.hpp",
            configuration=Configuration(ParsingConfiguration(language_version=LanguageStandard.CPP_20))
        )
        self.comments_factory = CommentsFactory(self.source_file)

    def test_function_comments(self):
        function = self.source_file.content[0]
        comment = self.comments_factory.get_upper_comment(function.text_source)
        self.assertEqual(comment, self.comments_factory.comments[0])

        function = self.source_file.content[1]
        comment = self.comments_factory.get_upper_comment(function.text_source)
        self.assertEqual(comment, self.comments_factory.comments[1])

        function = self.source_file.content[2]
        comment = self.comments_factory.get_upper_comment(function.text_source)
        self.assertEqual(comment, self.comments_factory.comments[2])

        function = self.source_file.content[3]
        comment = self.comments_factory.get_upper_comment(function.text_source)
        self.assertEqual(comment.begin.col, self.comments_factory.comments[3].begin.col)
        self.assertEqual(comment.begin.row, self.comments_factory.comments[3].begin.row)
        self.assertEqual(comment.end.col, self.comments_factory.comments[5].end.col)
        self.assertEqual(comment.end.row, self.comments_factory.comments[5].end.row)

    def test_functions_comments(self):
        function = self.source_file.content[4]
        comment = self.comments_factory.get_upper_comment(function.text_source)
        self.assertEqual(comment, self.comments_factory.comments[6])

        function = self.source_file.content[5]
        comment = self.comments_factory.get_upper_comment(function.text_source)
        self.assertEqual(comment, self.comments_factory.comments[7])

        function = self.source_file.content[6]
        comment = self.comments_factory.get_upper_comment(function.text_source)
        self.assertEqual(comment, self.comments_factory.comments[8])

    def test_class_core_comments(self):
        class_info = self.source_file.content[7]
        comment = self.comments_factory.get_upper_comment(class_info.text_source)
        self.assertEqual(comment, self.comments_factory.comments[9])

        class_info = self.source_file.content[8]
        comment = self.comments_factory.get_upper_comment(class_info.text_source)
        self.assertEqual(comment, self.comments_factory.comments[10])

    def test_namespace_comments(self):
        namespace = self.source_file.content[9]
        comment = self.comments_factory.get_upper_comment(namespace.text_source)
        self.assertEqual(comment, self.comments_factory.comments[11])

    def test_global_var_comments(self):
        global_var = self.source_file.content[10]
        comment = self.comments_factory.get_upper_comment(global_var.text_source)
        self.assertEqual(comment, self.comments_factory.comments[12])

    def test_enum_comments(self):
        enum_info = self.source_file.content[11]
        comment = self.comments_factory.get_upper_comment(enum_info.text_source)
        self.assertEqual(comment, self.comments_factory.comments[13])

    def test_union_comments(self):
        union = self.source_file.content[12]
        comment = self.comments_factory.get_upper_comment(union.text_source)
        self.assertEqual(comment, self.comments_factory.comments[14])

    def test_typedef_comments(self):
        typedef = self.source_file.content[13]
        comment = self.comments_factory.get_upper_comment(typedef.text_source)
        self.assertEqual(comment, self.comments_factory.comments[15])

    def test_class_members_comments(self):
        class_info = self.source_file.content[14]
        member = class_info.content[1]
        comment = self.comments_factory.get_upper_comment(member.text_source)
        self.assertEqual(comment, self.comments_factory.comments[16])
        member = class_info.content[2]
        comment = self.comments_factory.get_upper_comment(member.text_source)
        self.assertEqual(comment, self.comments_factory.comments[17])

    def test_enum_values_comments(self):
        enum_info = self.source_file.content[15]
        value_1 = enum_info.values[0]
        value_2 = enum_info.values[1]
        value_3 = enum_info.values[2]
        self.assertEqual(self.comments_factory.get_upper_comment(value_1.text_source), None)
        self.assertEqual(self.comments_factory.get_upper_comment(value_2.text_source),
                         self.comments_factory.comments[18])
        self.assertEqual(self.comments_factory.get_upper_comment(value_3.text_source), None)

    def test_concept_comments(self):
        concept_1 = self.source_file.content[16]
        comment = self.comments_factory.get_upper_comment(concept_1.text_source)
        self.assertEqual(comment, self.comments_factory.comments[20])

        concept_2 = self.source_file.content[17]
        comment = self.comments_factory.get_upper_comment(concept_2.text_source)
        self.assertEqual(comment, self.comments_factory.comments[21])


class TestCommentSourceFileAssigned(unittest.TestCase):

    def setUp(self):
        self.source = SourceFile(
            os.path.dirname(__file__) + r"/source_files/comments/complete_comments_file.hpp",
            configuration=Configuration(ParsingConfiguration(language_version=LanguageStandard.CPP_20))
        )

    def test_file_preamble(self):
        self.assertNotEqual(self.source.preamble, None)
        self.assertEqual(self.source.preamble.marker, CommentMarker.MULTI_LINE)
        self.assertEqual(len(self.source.preamble.text), 4)

    def test_file_flat_comments(self):
        element = self.source.content[0]
        comment: Comment = element.associated_comment
        self.assertEqual(len(comment.text), 1)
        self.assertEqual(comment.text[0], "test comment function")

        element = self.source.content[1]
        comment: Comment = element.associated_comment
        self.assertEqual(len(comment.text), 1)
        self.assertEqual(comment.text[0], "test comment function template")

        element = self.source.content[2]
        comment: Comment = element.associated_comment
        self.assertEqual(len(comment.text), 1)
        self.assertEqual(comment.text[0], "test comment function template spec")

        element = self.source.content[3]
        comment: Comment = element.associated_comment
        self.assertEqual(len(comment.text), 1)
        self.assertEqual(comment.text[0], "test comment class basic")

        element = self.source.content[4]
        comment: Comment = element.associated_comment
        self.assertEqual(len(comment.text), 1)
        self.assertEqual(comment.text[0], "test comment class template")

        element = self.source.content[5]
        comment: Comment = element.associated_comment
        self.assertEqual(len(comment.text), 1)
        self.assertEqual(comment.text[0], "test comment namespace")

        element = self.source.content[6]
        comment: Comment = element.associated_comment
        self.assertEqual(len(comment.text), 1)
        self.assertEqual(comment.text[0], "test comment global var")

        element = self.source.content[7]
        comment: Comment = element.associated_comment
        self.assertEqual(len(comment.text), 1)
        self.assertEqual(comment.text[0], "test comment enum")

        element = self.source.content[8]
        comment: Comment = element.associated_comment
        self.assertEqual(len(comment.text), 1)
        self.assertEqual(comment.text[0], "test comment union")

        element = self.source.content[9]
        comment: Comment = element.associated_comment
        self.assertEqual(len(comment.text), 1)
        self.assertEqual(comment.text[0], "test comment typedef")

        element = self.source.content[10]
        comment: Comment = element.associated_comment
        self.assertEqual(len(comment.text), 1)
        self.assertEqual(comment.text[0], "Test comment for concept")

    def test_file_nested_comments_simple_class(self):
        class_info = self.source.content[11]
        member = class_info.content[1]
        comment: Comment = member.associated_comment
        self.assertEqual(len(comment.text), 2)
        self.assertEqual(comment.text[0], "Test doc for constructor 1")
        self.assertEqual(comment.text[1], "Test doc for constructor 2")
        member = class_info.content[2]
        comment: Comment = member.associated_comment
        self.assertEqual(comment, None)
        member = class_info.content[3]
        comment: Comment = member.associated_comment
        self.assertEqual(len(comment.text), 1)
        self.assertEqual(comment.text[0], "simple field doc")

    def test_file_nested_comments_enum_values(self):
        enum_info = self.source.content[12]
        self.assertEqual(enum_info.values[0].associated_comment, None)
        self.assertEqual(enum_info.values[2].associated_comment, None)
        comment: Comment = enum_info.values[1].associated_comment
        self.assertEqual(len(comment.text), 1)
        self.assertEqual(comment.text[0], "test doc enum")


class TestCommentConfigurationAndFormatting(unittest.TestCase):

    def setUp(self):
        self.source = SourceFile(os.path.dirname(__file__) + r"/source_files/comments/comment_config.hpp")
        self.comments_factory = CommentsFactory(self.source)

    def test_comment_indentation(self):
        self.assertEqual(self.comments_factory.comments[0].text, ["  simple comment 1.1"])
        self.assertEqual(self.comments_factory.comments[1].text, ["simple comment 1.2"])
        self.assertEqual(self.comments_factory.comments[2].text, ["simple comment 2"])
        self.assertEqual(self.comments_factory.comments[3].text, [" simple comment 3"])

    def test_comment_remove_asterisks(self):
        self.source.configuration.parsing.comments.remove_asterisks = True
        self.assertEqual(self.comments_factory.comments[4].text[0], "test 1")
        self.assertEqual(self.comments_factory.comments[4].text[1], " test 2")

    def test_comment_keep_asterisks(self):
        self.source.configuration.parsing.comments.remove_asterisks = False
        self.assertEqual(self.comments_factory.comments[4].text[0], "*test 1")
        self.assertEqual(self.comments_factory.comments[4].text[1], "* test 2")

    def test_comment_remove_first_and_last_line(self):
        self.source.configuration.parsing.comments.remove_blank_lines = True
        self.assertEqual(len(self.comments_factory.comments[4].text), 2)

    def test_comment_pass_first_and_last_line(self):
        self.source.configuration.parsing.comments.remove_blank_lines = False
        self.assertEqual(len(self.comments_factory.comments[4].text), 4)
