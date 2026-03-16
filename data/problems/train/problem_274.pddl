

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b8)
(ontable b3)
(on b4 b9)
(on b5 b10)
(on b6 b5)
(ontable b7)
(on b8 b1)
(on b9 b2)
(on b10 b11)
(on b11 b7)
(clear b3)
(clear b4)
)
(:goal
(and
(on b1 b9)
(on b3 b2)
(on b4 b8)
(on b6 b10)
(on b8 b6)
(on b9 b3)
(on b10 b1)
(on b11 b4))
)
)


