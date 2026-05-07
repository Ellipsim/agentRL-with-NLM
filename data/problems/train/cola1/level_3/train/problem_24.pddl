

(define (problem BW-rand-5)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 - block)
(:init
(handempty)
(ontable b1)
(on b2 b3)
(ontable b3)
(on b4 b1)
(on b5 b2)
(clear b4)
(clear b5)
)
(:goal
(and
(on b1 b4)
(on b3 b2)
(on b4 b3))
)
)


