

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b9)
(ontable b2)
(ontable b3)
(on b4 b1)
(on b5 b6)
(on b6 b10)
(ontable b7)
(on b8 b11)
(on b9 b2)
(on b10 b12)
(on b11 b5)
(on b12 b3)
(clear b4)
(clear b7)
(clear b8)
)
(:goal
(and
(on b1 b9)
(on b2 b8)
(on b5 b2)
(on b6 b12)
(on b8 b6)
(on b9 b11)
(on b10 b4)
(on b11 b10)
(on b12 b7))
)
)


