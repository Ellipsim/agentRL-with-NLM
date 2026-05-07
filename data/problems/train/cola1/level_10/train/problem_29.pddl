

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b8)
(on b4 b12)
(on b5 b7)
(on b6 b9)
(on b7 b2)
(on b8 b4)
(on b9 b3)
(on b10 b5)
(on b11 b6)
(ontable b12)
(clear b1)
(clear b10)
(clear b11)
)
(:goal
(and
(on b1 b5)
(on b3 b10)
(on b4 b8)
(on b5 b9)
(on b6 b1)
(on b7 b12)
(on b9 b3)
(on b10 b11)
(on b12 b4))
)
)


