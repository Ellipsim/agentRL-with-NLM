

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(ontable b1)
(on b2 b8)
(on b3 b6)
(on b4 b3)
(on b5 b4)
(on b6 b1)
(ontable b7)
(on b8 b7)
(on b9 b5)
(clear b2)
(clear b9)
)
(:goal
(and
(on b3 b9)
(on b4 b8)
(on b5 b6)
(on b6 b1))
)
)


