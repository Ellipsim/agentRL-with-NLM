

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b7)
(on b2 b10)
(ontable b3)
(on b4 b9)
(on b5 b2)
(on b6 b3)
(on b7 b6)
(on b8 b1)
(on b9 b5)
(ontable b10)
(clear b4)
(clear b8)
)
(:goal
(and
(on b2 b10)
(on b3 b6)
(on b5 b7)
(on b6 b9)
(on b7 b2)
(on b8 b1)
(on b9 b8)
(on b10 b4))
)
)


