

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b7)
(on b3 b1)
(on b4 b9)
(on b5 b4)
(on b6 b5)
(ontable b7)
(ontable b8)
(ontable b9)
(clear b2)
(clear b3)
(clear b6)
)
(:goal
(and
(on b1 b6)
(on b3 b5)
(on b4 b7)
(on b5 b2)
(on b6 b9)
(on b8 b4)
(on b9 b8))
)
)


