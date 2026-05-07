

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(ontable b1)
(on b2 b8)
(on b3 b5)
(ontable b4)
(ontable b5)
(on b6 b3)
(on b7 b1)
(on b8 b4)
(on b9 b6)
(clear b2)
(clear b7)
(clear b9)
)
(:goal
(and
(on b1 b5)
(on b2 b8)
(on b4 b1)
(on b5 b2)
(on b6 b4)
(on b7 b9)
(on b9 b6))
)
)


