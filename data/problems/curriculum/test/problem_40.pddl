

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(ontable b1)
(on b2 b5)
(on b3 b2)
(on b4 b6)
(on b5 b1)
(on b6 b3)
(ontable b7)
(on b8 b7)
(on b9 b8)
(clear b4)
(clear b9)
)
(:goal
(and
(on b1 b4)
(on b3 b7)
(on b6 b2)
(on b7 b6)
(on b8 b5)
(on b9 b1))
)
)


