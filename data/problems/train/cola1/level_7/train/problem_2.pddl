

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(ontable b1)
(on b2 b1)
(on b3 b6)
(ontable b4)
(on b5 b7)
(on b6 b4)
(on b7 b3)
(ontable b8)
(clear b2)
(clear b5)
(clear b8)
)
(:goal
(and
(on b1 b5)
(on b2 b8)
(on b3 b2)
(on b6 b3))
)
)


