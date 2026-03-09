(define (problem bw-simple)
  (:domain blocksworld)
  (:objects obj0 obj1 - block)
  (:init
    (ontable obj1)
    (on obj0 obj1)
    (clear obj0)
    (handempty))
  (:goal (and
    (on obj1 obj0))))