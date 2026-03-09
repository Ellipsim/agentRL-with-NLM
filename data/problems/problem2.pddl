(define (problem bw-tower)
  (:domain blocksworld)
  (:objects obj0 obj1 obj2 - block)
  (:init
    (ontable obj0)
    (ontable obj1)
    (ontable obj2)
    (clear obj0)
    (clear obj1)
    (clear obj2)
    (handempty))
  (:goal (and
    (on obj0 obj1)
    (on obj1 obj2))))