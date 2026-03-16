

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(ontable b1)
(on b2 b5)
(on b3 b9)
(on b4 b2)
(on b5 b1)
(on b6 b7)
(on b7 b10)
(ontable b8)
(on b9 b4)
(on b10 b3)
(on b11 b8)
(clear b6)
(clear b11)
)
(:goal
(and
(on b1 b3)
(on b2 b10)
(on b3 b5)
(on b4 b11)
(on b7 b1)
(on b8 b6)
(on b9 b8)
(on b10 b9)
(on b11 b2))
)
)


