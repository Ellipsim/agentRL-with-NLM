

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b5)
(ontable b2)
(on b3 b1)
(on b4 b7)
(ontable b5)
(on b6 b8)
(on b7 b2)
(on b8 b3)
(clear b4)
(clear b6)
)
(:goal
(and
(on b2 b6)
(on b4 b1)
(on b5 b3)
(on b6 b8)
(on b7 b2)
(on b8 b4))
)
)


