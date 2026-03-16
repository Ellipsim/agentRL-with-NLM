

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b5)
(ontable b2)
(on b3 b10)
(on b4 b3)
(on b5 b2)
(on b6 b8)
(on b7 b9)
(on b8 b4)
(ontable b9)
(on b10 b7)
(on b11 b1)
(clear b6)
(clear b11)
)
(:goal
(and
(on b1 b3)
(on b2 b11)
(on b3 b9)
(on b4 b7)
(on b5 b1)
(on b7 b2)
(on b9 b8)
(on b10 b6)
(on b11 b10))
)
)


