from table import Table
import os


class DictTree(dict):
    """
    A class to work with a dict whose keys are tuples as if this dict was a dictionary of dictionaries of dictionaries...
    When trying to look up a value with key (=tuple) and this tuple is partially contained in other keys (=tuples) than
    a DictTree with only those truncated keys is returned.
    """

    def __getitem__(self, tpl):
        if not isinstance(tpl, tuple):
            tpl = (tpl,)
        if tpl in self.keys():
            return super(DictTree, self).__getitem__(tpl)
        else:
            kvals = [(key[len(tpl):], value) for key, value in self.items() if len(key) >= len(tpl) and key[0:len(tpl)] == tpl]
            if kvals:
                return DictTree(kvals)
            else:
                raise KeyError

    def as_table(self, name):

        "Return a table from two uppermost layers of the DictTree"


        len1_keys = [key for key in self.keys() if len(key)==1]
        len2_keys = [key for key in self.keys() if len(key)==2]

        pt = Table(name= name,left_upper='Properties')
        for k in len1_keys:
            pt.append('', k[0], self[k])

        vt = Table(name=name, left_upper='Values')
        for k in len2_keys:
            vt.append(k[0], k[1], self[k])

        return pt.sort(), vt.sort()

    def make_tables(self):
        """Makes a table from each level within the DictTree"""
        max_level = max(map(len, self.keys()))
        tables = list()
        for i in range(0, max_level):
            for key in sorted(list(set([k[0:i] for k in self.keys()]))):
                T = self[key]
                if isinstance(T, DictTree):
                    a, b = T.as_table(" || ".join(map(str,key)))
                    if not a.is_empty() and i == 0:
                        tables.append(a)
                    if not b.is_empty():
                        tables.append(b)
        return tables

    def html_tables(self, path, filename):
        """writes all ables to a filename.html in path"""
        if not os.path.isdir(path):
            os.makedirs(path)

        s = """<!DOCTYPE html>\n<html>\n<head>\n<title>%s</title>\n<style>
        th, td {
            border: 1px solid #888;
            padding: 5px;
        }
        td {
            text-align: right;
            white-space: nowrap;
        }
        table {
            padding: 1px;
        }
        </style>\n</head>\n<body>
        """ % filename

        for t in self.make_tables():
            s += '<h4>{}</h4>'.format(t.name)
            s += t.to_html()
            s += '<br>'

        s += "</body>\n</html>"

        with open(path+'\\%s.html' % filename, 'w') as f:
            f.write(s)