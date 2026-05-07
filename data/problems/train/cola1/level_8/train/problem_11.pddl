

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(ontable b1)
(on b2 b8)
(on b3 b2)
(on b4 b6)
(ontable b5)
(on b6 b9)
(on b7 b1)
(on b8 b4)
(on b9 b5)
(clear b3)
(clear b7)
)
(:goal
(and
(on b1 b7)
(on b4 b9)
(on b5 b8)
(on b7 b2)
(on b8 b3)
(on b9 b1))
)
)


