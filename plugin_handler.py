'''plugin handling functions'''

import re

#from plugins.latest_articles.latest_articles import latest_articles

# Settings
# --> Pandoc adds newlines into the div now...
# (My way of substitution is simple but it seems also fragile...)
# ==> adding newlines here to fix it, quick but still ugly...
# --> maybe use some sort of python temporary filename
#PLUGIN_PLACEHOLDER = '<div id="placeholder">\n<p>\nSomething\n</p>\n</div>'
PLUGIN_PLACEHOLDER='d8a2cabb38c68700bdef0112a5f2a35e'

def plugin_cdata_handler(page, cdata_blocks):
    '''Receive the cdata blocks and forward them to the appropriate plugin.'''
    plugin_blocks = []
    plugin_pandoc_opts = []

    for block in cdata_blocks:
        pandoc_opts = []
        # extract plugin name and content from cdata block
        block_split = block.split(']')
        plugin_name = block_split[0].strip('[[').strip()

        plugin_in = block_split[1].strip().strip('[').strip()

        # here now we forward the blocks to the appropriate plugins
        # Each plugin needs an entry here !

        if plugin_name == 'IMAGETHUMBS':
            plugin_out = imagethumbs(page)

        #elif plugin_name = 'PLUGIN_NAME':
        #	plugin_out, pandoc_opts = plugin_function(plugin_content

        # if no plugin is found return the raw content
        else:
            print("Warning: Plugin not found:", plugin_name)
            plugin_out = block

        plugin_blocks.append(plugin_out)
        plugin_pandoc_opts.extend(pandoc_opts)

    # (debug-print)
    #print("plugin blocks pdf plugin_handler: ", plugin_blocks_pdf)

    return plugin_blocks, plugin_pandoc_opts


def get_cdata(text):
    '''Get the cdata blocks and replace them by a placeholder.

Return the text and the blocks.'''
    #
    # the regex for cdata
    # should be <![TYPE[DATA]]> ==> changed to [[ TYPE ] [ DATA ]]
    re_cdata=re.compile(r'\[\[.+?\]\]', re.DOTALL)
    cdata_blocks=re_cdata.findall(text)

    text_rep=text
    for block in cdata_blocks:
        text_rep=text_rep.replace(block, PLUGIN_PLACEHOLDER)

    # (debug-info)
    #print('Cdata blocks:', cdata_blocks)
    #print('Text rep:', text_rep)

    return text_rep, cdata_blocks


def back_substitute(text, cdata_blocks):
    '''Back substitution of plugin content.'''
    for block in cdata_blocks:
        # (debug-info)
        #print('Block:', block)
        text=text.replace('<p>' + PLUGIN_PLACEHOLDER + '</p>', block, 1)

    # (debug-info)
    #print('Text:', text)

    return text
