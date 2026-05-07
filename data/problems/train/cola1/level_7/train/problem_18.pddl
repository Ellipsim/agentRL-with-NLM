

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(ontable b1)
(on b2 b1)
(on b3 b2)
(on b4 b9)
(ontable b5)
(ontable b6)
(on b7 b3)
(on b8 b7)
(on b9 b8)
(clear b4)
(clear b5)
(clear b6)
)
(:goal
(and
(on b1 b2)
(on b2 b7)
(on b3 b1)
(on b5 b3)
(on b6 b8)
(on b7 b4))
)
)


