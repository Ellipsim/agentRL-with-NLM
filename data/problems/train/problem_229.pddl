

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b4)
(ontable b2)
(ontable b3)
(on b4 b8)
(on b5 b6)
(ontable b6)
(ontable b7)
(on b8 b3)
(clear b1)
(clear b2)
(clear b5)
(clear b7)
)
(:goal
(and
(on b2 b1)
(on b5 b2)
(on b6 b8)
(on b7 b6)
(on b8 b3))
)
)


