

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b3)
(on b2 b8)
(on b3 b5)
(on b4 b9)
(on b5 b4)
(ontable b6)
(ontable b7)
(on b8 b6)
(ontable b9)
(clear b1)
(clear b2)
(clear b7)
)
(:goal
(and
(on b2 b7)
(on b4 b9)
(on b7 b8)
(on b8 b1)
(on b9 b2))
)
)


