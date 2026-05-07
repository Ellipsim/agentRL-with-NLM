

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b4)
(ontable b2)
(on b3 b1)
(ontable b4)
(on b5 b3)
(on b6 b5)
(on b7 b6)
(ontable b8)
(on b9 b2)
(clear b7)
(clear b8)
(clear b9)
)
(:goal
(and
(on b2 b8)
(on b3 b6)
(on b5 b4)
(on b6 b7)
(on b7 b9)
(on b8 b5)
(on b9 b2))
)
)


