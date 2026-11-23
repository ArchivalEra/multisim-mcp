import schemdraw
import schemdraw.elements as elm

d = schemdraw.Drawing()
# Let's inspect elm.SourceControlledI
# Why is the diamond filled with black and the arrow not visible?
# Look at SourceControlled definition:
s = elm.SourceControlledI()
print("s fill:", s.params.get('fill'))
for seg in s.segments:
    print(seg, seg.path, getattr(seg, 'arrow', None), getattr(seg, 'fill', None))
