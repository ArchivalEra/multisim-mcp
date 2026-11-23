import inspect
import schemdraw.elements as elm

print("SourceControlledI segments:")
s = elm.SourceControlledI()
for i, seg in enumerate(s.segments):
    print(f"[{i}] {type(seg)} path={seg.path} arrow={getattr(seg, 'arrow', None)}")
print("="*40)
print("SourceControlled segments:")
sc = elm.SourceControlled()
for i, seg in enumerate(sc.segments):
    print(f"[{i}] {type(seg)} path={seg.path}")
