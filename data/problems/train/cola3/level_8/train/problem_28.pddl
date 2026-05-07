

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b5)
(on b2 b8)
(ontable b3)
(ontable b4)
(on b5 b9)
(on b6 b1)
(ontable b7)
(on b8 b4)
(on b9 b3)
(clear b2)
(clear b6)
(clear b7)
)
(:goal
(and
(on b1 b3)
(on b2 b1)
(on b3 b5)
(on b4 b2)
(on b8 b9)
(on b9 b6))
)
)


