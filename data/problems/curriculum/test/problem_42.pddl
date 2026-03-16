

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b6)
(ontable b4)
(on b5 b8)
(on b6 b2)
(on b7 b4)
(on b8 b1)
(on b9 b5)
(clear b3)
(clear b7)
(clear b9)
)
(:goal
(and
(on b1 b2)
(on b2 b9)
(on b3 b1)
(on b5 b8)
(on b6 b7)
(on b8 b3)
(on b9 b4))
)
)


