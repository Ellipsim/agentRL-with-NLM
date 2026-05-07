

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b3)
(on b2 b5)
(on b3 b9)
(on b4 b7)
(on b5 b4)
(on b6 b8)
(ontable b7)
(ontable b8)
(ontable b9)
(clear b1)
(clear b2)
(clear b6)
)
(:goal
(and
(on b2 b1)
(on b4 b8)
(on b5 b9)
(on b7 b3)
(on b9 b2))
)
)


