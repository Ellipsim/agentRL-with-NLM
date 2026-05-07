

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b5)
(on b3 b4)
(on b4 b2)
(ontable b5)
(on b6 b1)
(ontable b7)
(on b8 b7)
(ontable b9)
(clear b3)
(clear b6)
(clear b9)
)
(:goal
(and
(on b1 b6)
(on b3 b7)
(on b4 b1)
(on b5 b3)
(on b6 b9)
(on b7 b2)
(on b9 b8))
)
)


