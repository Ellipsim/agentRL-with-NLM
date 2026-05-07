

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b8)
(on b3 b10)
(on b4 b9)
(ontable b5)
(on b6 b5)
(on b7 b1)
(on b8 b3)
(on b9 b2)
(ontable b10)
(clear b4)
(clear b7)
)
(:goal
(and
(on b1 b8)
(on b3 b4)
(on b5 b6)
(on b6 b9)
(on b7 b3)
(on b8 b7)
(on b9 b2))
)
)


